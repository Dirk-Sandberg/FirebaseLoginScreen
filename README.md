# FirebaseLoginScreen
Complete login screen with backend included for Kivy apps using Firebase for
user authentication.

This package lets you essentially drop a functional login screen into your app
within seconds.

<h1>Features:</h1>

- Create account
- Email verification for new accounts
- Sign in to account
- Log out of account
- Reset password
- Automatically signs users in upon app launch if an account has already been created.

If a user has already signed in, it will store their login data and
automatically sign them in the next time around. In this case, the login screens
will not be shown, and your app will immediately do whatever you have coded it
to do in the `on_login_success` function of the `FirebaseLoginScreen`.

Usage
-

<b>Install from Pypi</b>

`pip install firebaseloginscreen`

<h5>Add the FirebaseLoginScreen widget to your ScreenManager</h5>

In the kv file where you want to use the login screen, import the `FirebaseLoginScreen` widget:

    #:import FirebaseLoginScreen firebaseloginscreen.firebaseloginscreen.FirebaseLoginScreen

Then add the `FirebaseLoginScreen` widget to your `ScreenManager` class, wherever that may be. Here's a snippet
of the code you should add to your `ScreenManager`:

        FirebaseLoginScreen:
            id: firebase_login_screen
            name: "firebase_login_screen"
            debug: True
            remember_user: True
            require_email_verification: True
            web_api_key: "your_web_api_key_from_firebase" # Found in Firebase -> Project Settings -> Web API Key
            background: "background.jpg"
            on_login_success:
                # Defining this function lets you program what to do when the
                # user has logged in (probably you'll want to change screens)!
                # Get the important user info
                app.user_localId = self.localId
                app.user_idToken = self.idToken

Make sure the FirebaseLoginScreen is the first screen in your `ScreenManager`.

Variables you can set when you instantiate the `FirebaseLoginScreen`:
| variable name  | required? | Description | Default |
| ------------- | ------------- | ------------- |
| debug  | No  | Will print a bunch of helpful output. | False |
| remember_user  | No  | Will remember the last user to sign in and automatically sign them in when they open the app. | True |
| require_email_verification | No | Sends new users a verification email before they can sign in. | True |
| web_api_key| Yes | Your Firebase project's web api key. | None |
| on_login_success | Yes | This function is fired when the user successfully logs in OR out. | None |
| background | No | The path to an image that will be the background for the login screen. | None |

Check out the examples folder in this Github repo if you want to see an example of using the FirebaseLoginScreen.

Need help figuring out the setup related to Firebase? Check out these instructions.

# Notes from the author
You should define the `on_login_success` function to execute whatever code you
want once a user has logged in. Probably you'll want to 1) Retrieve some data
from Firebase and 2) switch to a different screen in your `ScreenManager`.

Typically, when making requests to your database to get data for your user, you
identify the user by their `localId`. You can use the `idToken` to authenticate
a user's request to the database if you have set up Firebase <b>Rules</b>. Both
of these variables are automatically retrieved for you by `FirebaseLoginScreen`.<br>
    

Suggestions
-

If your app takes a long time to start up, you may need to set the `web_api_key`
from python instead of in the kv language. You need to set it in the `on_start`
method of your `App` class. Haven't fully characterized this race condition yet. 


# Future Features
Boolean SMS Verification (for phone sign ins) 
Sign in method choice
    email, phone
