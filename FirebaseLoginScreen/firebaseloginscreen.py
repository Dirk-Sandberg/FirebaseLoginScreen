from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
# Import the screens used to log the user in
from welcomescreen import WelcomeScreen
from signinscreen import SignInScreen
from createaccountscreen import CreateAccountScreen

# Python imports
from json import dumps
from os.path import exists


class FirebaseLoginScreen(Screen, EventDispatcher):
    # Configurable UI attributes
    primary_color = (0, 1, 1)
    secondary_color = (0, .2, 1)
    tertiary_color = (1, 0, 0)
    login_success = BooleanProperty(False)

    # Firebase Project meta info - MUST BE CONFIGURED BY DEVELOPER
    web_api_key = StringProperty()  # From Settings tab in Firebase project

    # Firebase Authentication Credentials - what developers want to retrieve
    #email = ""
    refresh_token = ""
    localId = ""
    idToken = ""

    # Private properties used to update parts of the login screen
    sign_up_msg = StringProperty()
    sign_in_msg = StringProperty()
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(FirebaseLoginScreen, self).__init__(**kwargs)



    def on_login_success(self, *args):
        """Overwrite this method to switch to your app's home screen.
        """
        print("Logged in successfully", args)

    def on_web_api_key(self, *args):
        """When the web api key is set, look for an existing account in local
        memory.

        :return:
        """
        # Try to load the users info if they've already created an account
        self.refresh_token_file = App.get_running_app().user_data_dir + "refresh_token.txt"
        if exists(self.refresh_token_file):
            self.load_saved_account()

    def sign_up(self, email, password):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to sign the user up with their email and
        password.
        """
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
        signup_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": "true"})

        UrlRequest(signup_url, req_body=signup_payload,
                   on_success=self.successful_login,
                   on_failure=self.sign_up_failure,
                   on_error=self.sign_up_error)

    def successful_login(self, urlrequest, log_in_data):
        """Collects info from Firebase upon successfully registering a new user.
        """
        self.refresh_token = log_in_data['refreshToken']
        self.localId = log_in_data['localId']
        self.idToken = log_in_data['idToken']
        self.save_refresh_token(self.refresh_token)
        self.login_success = True
        print(log_in_data)

    def sign_up_failure(self, urlrequest, failure_data):
        self.email_exists = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        # Check if the error msg is the same as the last one
        if msg == self.sign_up_msg:
            msg = " " + msg + " "
            # Need to modify it somehow to make the error popup display
        self.sign_up_msg = msg
        if msg == "Email exists":
            self.email_exists = True

    def sign_up_error(self, *args):
        print("Sign up Error")
        print(args)

    def sign_in(self, email, password):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to sign the user in with their email and
        password.
        """
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
        sign_in_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(sign_in_url, req_body=sign_in_payload,
                   on_success=self.successful_login,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error)

    def sign_in_failure(self, urlrequest, failure_data):
        self.email_not_found = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        # Check if the error msg is the same as the last one
        if msg == self.sign_in_msg:
            msg = " " + msg + " "
            # Need to modify it somehow to make the error popup display
        self.sign_in_msg = msg
        print(msg)
        if msg == "Email not found":
            self.email_not_found = True

    def sign_in_error(self, *args):
        print("Sign in error")
        print(args)

    def reset_password(self, email):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to reset a user's password from their email.
        """
        reset_pw_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.web_api_key
        reset_pw_data = dumps({"email": email, "requestType": "PASSWORD_RESET"})

        UrlRequest(reset_pw_url, req_body=reset_pw_data,
                   on_success=self.successful_reset,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error)

    def successful_reset(self, urlrequest, reset_data):
        self.sign_in_msg = "Reset password instructions sent to your email."

    def save_refresh_token(self, refresh_token):
        with open(self.refresh_token_file, "w") as f:
            f.write(refresh_token)

    def load_refresh_token(self):
        with open(self.refresh_token_file, "r") as f:
            self.refresh_token = f.read()

    def load_saved_account(self):
        self.load_refresh_token()
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
        refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
        UrlRequest(refresh_url, req_body=refresh_payload,
                   on_success=self.successful_account_load,
                   on_failure=self.failed_account_load,
                   on_error=self.failed_account_load)

    def successful_account_load(self, urlrequest, loaded_data):
        self.idToken = loaded_data['id_token']
        self.localId = loaded_data['user_id']
        self.login_success = True

    def failed_account_load(self, *args):
        print("Failed to load an account")
        print(args)


