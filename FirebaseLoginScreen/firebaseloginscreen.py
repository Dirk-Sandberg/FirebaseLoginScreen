from kivy.uix.screenmanager import Screen

# Import the screens used to log the user in
from welcomescreen import WelcomeScreen
from signinscreen import SignInScreen
from createaccountscreen import CreateAccountScreen
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher


class FirebaseLoginScreen(Screen, EventDispatcher):
    primary_color = (0, 1, 1)
    secondary_color = (0, .2, 1)
    tertiary_color = (1, 0, 0)
    login_success = BooleanProperty(False)

    def on_login_success(self, *args):
        """Overwrite this method to switch to your screen.
        """
        print("Logged in successfully", args)

    def sign_up(self, email, password):
        """If you don't want to use Firebase, just overwrite this method and
        do whatever you need to do to sign the user up with their email and
        password.
        """
        print("sign up")

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

