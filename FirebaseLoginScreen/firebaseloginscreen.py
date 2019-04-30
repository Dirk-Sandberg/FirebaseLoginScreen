from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest

# Import the screens used to log the user in
from welcomescreen import WelcomeScreen
from signinscreen import SignInScreen
from createaccountscreen import CreateAccountScreen

# Python imports
from json import dumps


class FirebaseLoginScreen(Screen, EventDispatcher):
    # Configurable UI attributes
    primary_color = (0, 1, 1)
    secondary_color = (0, .2, 1)
    tertiary_color = (1, 0, 0)
    login_success = BooleanProperty(False)

    # Firebase Project meta info - MUST BE CONFIGURED BY DEVELOPER
    web_api_key = ""  # From Settings tab in Firebase project

    # Firebase Authentication Credentials - what developers want to retrieve
    email = ""
    user_token = ""

    # Private properties used to update parts of the login screen
    sign_up_error_msg = StringProperty()
    email_exists = BooleanProperty(False)

    def on_login_success(self, *args):
        """Overwrite this method to switch to your screen.
        """
        print("Logged in successfully", args)

    def sign_up(self, email, password):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to sign the user up with their email and
        password.
        """
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
        signup_payload = dumps({"email": email, "password": password, "returnSecureToken": "true"})

        sign_up_request = UrlRequest(signup_url, req_body=signup_payload,
                                     on_success=self.sign_up_success,
                                     on_failure=self.sign_up_failure,
                                     on_error=self.sign_up_error)

    def sign_up_success(self, *args):
        """Collects info from Firebase upon successfully registering a new user.
        """
        sign_up_data = args[1]
        print(sign_up_data)
        self.refresh_token = sign_up_data['refreshToken']
        self.localId = ''
        self.idToken = ''
        self.email = sign_up_data['email']

    def sign_up_error(self, *args):
        print("Error")
        print(args)

    def sign_up_failure(self, *args):
        failure_data = args[1]
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        # Check if the error msg is the same as the last one
        if msg == self.sign_up_error_msg:
            msg = " " + msg + " "
            # Need to modify it somehow to make the error popup display
        self.sign_up_error_msg = msg
        if msg == "Email exists":
            self.email_exists = True



    def sign_in(self, email, password):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to sign the user in with their email and
        password.
        """
        print("Sign In")
        self.login_success = True # automatically triggers on_login_success, which users can overwrite

    def reset_password(self, email):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to reset a user's password from their email.
        """
        print("Reset pw")

