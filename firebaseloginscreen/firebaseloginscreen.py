from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
import certifi

# KivyMD imports
from kivymd.toast import toast

# Python imports
import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps
import os.path

# Load the kv files
folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/signinscreen.kv")
Builder.load_file(folder + "/signupscreen.kv")
Builder.load_file(folder + "/welcomescreen.kv")
Builder.load_file(folder + "/loadingpopup.kv")
Builder.load_file(folder + "/firebaseloginscreen.kv")

# Import the screens used to log the user in
from welcomescreen import WelcomeScreen
from signinscreen import SignInScreen
from signupscreen import SignUpScreen



class FirebaseLoginScreen(Screen, EventDispatcher):
    """Use this widget as a complete module to incorporate Firebase user
    authentication in your app. To use this module, instantiate the login screen
    in the KV language like so:
    FirebaseLoginScreen:
        web_api_key: "your_firebase_web_api_key"
        debug: True # Not necessary, but will print out debug information
        on_login_success:
            # do something here

    NOTES:
    1) You MUST set the web api key or it is impossible for the login screen to
    function properly.
    2) You probably want to wrap the firebaseloginscreen in a ScreenManager.
    3) You probably want to switch screens to a Screen in your project once the
    user has logged in (write that code in the on_login_success function shown
    in the example above).
    """

    # Firebase Project meta info - MUST BE CONFIGURED BY DEVELOPER
    web_api_key = StringProperty()  # From Settings tab in Firebase project

    # Firebase Authentication Credentials - what developers want to retrieve
    refresh_token = ""
    localId = ""
    idToken = ""

    # Properties used to send events to update some parts of the UI
    login_success = BooleanProperty(False)  # Called upon successful sign in
    login_state = StringProperty("")
    sign_up_msg = StringProperty()
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)
    remember_user = BooleanProperty(True)
    require_email_verification = BooleanProperty(True)

    debug = False
    popup = Factory.LoadingPopup()
    popup.background = folder + "/transparent_image.png"

    def log_out(self):
        '''Clear the user's refresh token, marked them as not signed in, and
        go back to the welcome screen.
        '''
        with open(self.refresh_token_file, 'w') as f:
            f.write('')
        self.login_state = 'out'
        self.login_success = False
        self.refresh_token = ''
        self.ids.screen_manager.current = 'welcome_screen'
        # Clear text fields
        self.ids.sign_in_screen.ids.email.text = ''
        self.ids.sign_in_screen.ids.password.text = ''
        self.ids.sign_up_screen.ids.email.text = ''
        self.ids.sign_up_screen.ids.password.text = ''


    def on_login_success(self, screen_name, login_success_boolean):
        """Overwrite this method to switch to your app's home screen.
        """
        print("Testing", self.login_success, self.login_state)
        print("self.login_success=", login_success_boolean)

    def on_web_api_key(self, *args):
        """When the web api key is set, look for an existing account in local
        memory.
        """
        # Try to load the users info if they've already created an account
        self.refresh_token_file = App.get_running_app().user_data_dir + "/refresh_token.txt"
        if self.debug:
            print("Looking for a refresh token in:", self.refresh_token_file)
        if self.remember_user:
            print("REMEMBER USER IS TRUE")
            if os.path.exists(self.refresh_token_file):
                self.load_saved_account()

    def sign_up(self, email, password):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to sign the user up with their email and
        password.
        """
        if self.debug:
            print("Attempting to create a new account: ", email, password)
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
        signup_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": "true"})

        UrlRequest(signup_url, req_body=signup_payload,
                   on_success=self.successful_sign_up,
                   on_failure=self.sign_up_failure,
                   on_error=self.sign_up_error, ca_file=certifi.where())

    def successful_sign_up(self, request, result):
        if self.debug:
            print("Successfully signed up a user: ", result)
        self.hide_loading_screen()
        self.refresh_token = result['refreshToken']
        self.localId = result['localId']
        self.idToken = result['idToken']

        if self.require_email_verification:
            self.send_verification_email(result['email'])
            self.ids.screen_manager.current = 'sign_in_screen'

        else:
            self.save_refresh_token(self.refresh_token)
            self.login_state = 'in'
            self.login_success = True

    def sign_in_success(self, urlrequest, log_in_data):
        """Collects info from Firebase upon successfully registering a new user.
        """
        if self.debug:
            print("Successfully signed in a user: ", log_in_data)
        # User's email/password exist, but are they verified?
        self.hide_loading_screen()
        self.refresh_token = log_in_data['refreshToken']
        self.localId = log_in_data['localId']
        self.idToken = log_in_data['idToken']
        self.save_refresh_token(self.refresh_token)

        if self.require_email_verification:
            self.check_if_user_verified_email()
        else:
            self.login_state = 'in'
            self.login_success = True

    def sign_up_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to log in was
        invalid.
        """
        self.hide_loading_screen()
        self.email_exists = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        toast(msg)
        if msg == "Email exists":
            self.email_exists = True
        if self.debug:
            print("Couldn't sign the user up: ", failure_data)

    def sign_up_error(self, *args):
        self.hide_loading_screen()
        if self.debug:
            print("Sign up Error: ", args)

    def sign_in(self, email, password):
        """Called when the "Log in" button is pressed.

        Sends the user's email and password in an HTTP request to the Firebase
        Authentication service.
        """
        if self.debug:
            print("Attempting to sign user in: ", email, password)
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
        sign_in_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(sign_in_url, req_body=sign_in_payload,
                   on_success=self.sign_in_success,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def sign_in_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to create an
        account was invalid.
        """
        self.hide_loading_screen()
        self.email_not_found = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        toast(msg)
        if msg == "Email not found":
            self.email_not_found = True
        if self.debug:
            print("Couldn't sign the user in: ", failure_data)

    def sign_in_error(self, *args):
        self.hide_loading_screen()
        if self.debug:
            print("Sign in error", args)

    def reset_password(self, email):
        """Called when the "Reset password" button is pressed.

        Sends an automated email on behalf of your Firebase project to the user
        with a link to reset the password. This email can be customized to say
        whatever you want. Simply change the content of the template by going to
        Authentication (in your Firebase project) -> Templates -> Password reset
        """
        if self.debug:
            print("Attempting to send a password reset email to: ", email)
        reset_pw_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.web_api_key
        reset_pw_data = dumps({"email": email, "requestType": "PASSWORD_RESET"})

        UrlRequest(reset_pw_url, req_body=reset_pw_data,
                   on_success=self.successful_reset,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def successful_reset(self, urlrequest, reset_data):
        """Notifies the user that a password reset email has been sent to them.
        """
        self.hide_loading_screen()
        if self.debug:
            print("Successfully sent a password reset email", reset_data)
        toast("Reset password instructions sent to your email.")

    def save_refresh_token(self, refresh_token):
        """Saves the refresh token in a local file to enable automatic sign in
        next time the app is opened.
        """
        if self.debug:
            print("Saving the refresh token to file: ", self.refresh_token_file)
        with open(self.refresh_token_file, "w") as f:
            f.write(refresh_token)

    def load_refresh_token(self):
        """Reads the refresh token from local storage.
        """
        if self.debug:
            print("Loading refresh token from file: ", self.refresh_token_file)
        with open(self.refresh_token_file, "r") as f:
            self.refresh_token = f.read()

    def load_saved_account(self):
        """Uses the refresh token to get the user's idToken and localId by
        sending it as a request to Google/Firebase's REST API.

        Called immediately when a web_api_key is set and if the refresh token
        file exists.
        """
        if self.debug:
            print("Attempting to log in a user automatically using a refresh token.")
        self.load_refresh_token()
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
        refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
        UrlRequest(refresh_url, req_body=refresh_payload,
                   on_success=self.successful_account_load,
                   on_failure=self.failed_account_load,
                   on_error=self.failed_account_load, ca_file=certifi.where())

    def successful_account_load(self, urlrequest, loaded_data):
        """Sets the idToken and localId variables upon successfully loading an
        account using the refresh token.
        """
        self.hide_loading_screen()
        if self.debug:
            print("Successfully logged a user in automatically using the refresh token")
        self.idToken = loaded_data['id_token']
        self.localId = loaded_data['user_id']
        self.login_state = 'in'
        self.login_success = True

    def failed_account_load(self, *args):
        self.hide_loading_screen()
        if self.debug:
            print("Failed to load an account.", args)

    def sign_out(self):
        self.localId = ''
        self.idToken = ''
        self.clear_refresh_token_file()
        self.ids.screen_manager.current = 'welcome_screen'
        toast("Signed out")

    def clear_refresh_token_file(self):
        with open(self.refresh_token_file, 'w') as f:
            f.write('')

    def display_loading_screen(self, *args):
        self.popup.open()

    def hide_loading_screen(self, *args):
        self.popup.dismiss()

    def check_if_user_verified_email(self):
        """If :populate_realtime_db_with_id: is True, a verified=True record will
        be placed in this user's record.
        """

        if self.debug:
            print("Attempting to check if the user signed in has verified their email")
        check_email_verification_url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + self.web_api_key
        check_email_verification_data = dumps(
            {"idToken": self.idToken})

        UrlRequest(check_email_verification_url, req_body=check_email_verification_data,
                   on_success=self.got_verification_info,
                   on_failure=self.could_not_get_verification_info,
                   on_error=self.could_not_get_verification_info,
                   ca_file=certifi.where())

    def could_not_get_verification_info(self, request, result):
        if self.debug:
            print("could_not_get_verification_info", request, result)
        self.hide_loading_screen()
        toast("Failed to check email verification status.")

    def got_verification_info(self, request, result):
        if self.debug:
            print("got_verification_info", request, result)
        if result['users'][0]['emailVerified']:
            self.login_state = 'in'
            self.login_success = True
        else:
            toast("Your email is not verified yet.\n Please check your email.")

    def send_verification_email(self, email):
        """Sends a verification email.

        Sends an automated email on behalf of your Firebase project to the user
        with a link to verify their email. This email can be customized to say
        whatever you want. Simply change the content of the template by going to
        Authentication (in your Firebase project) -> Templates -> Email Address Verification

        This email verification can only be sent after a user has signed up.
        The email will contain a code that must be entered back into the
        app.
        """
        if self.debug:
            print("Attempting to send a email verification email to: ", email)
        verify_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + self.web_api_key
        verify_email_data = dumps(
            {"idToken": self.idToken, "requestType": "VERIFY_EMAIL"})

        UrlRequest(verify_email_url, req_body=verify_email_data,
                   on_success=self.successful_verify_email_sent,
                   on_failure=self.unsuccessful_verify_email_sent,
                   on_error=self.unsuccessful_verify_email_sent,
                   ca_file=certifi.where())

    def unsuccessful_verify_email_sent(self, *args):
        toast("Couldn't send email verification email")

    def successful_verify_email_sent(self, *args):
        toast("A verification email has been sent. \nPlease check your email.")
