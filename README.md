# FirebaseLoginScreen
Complete login screen with backend included for Kivy apps using Firebase for
user authentication.

This package lets you essentially drop a functional login screen into your app
within seconds.

<h1>Features:</h1>

- Create account
- Sign in to account
- Reset password
- Automatically signs users in upon app launch if an account has already been created.

If a user has already signed in, it will store their login data and
automatically sign them in the next time around. In this case, the login screens
will not be shown, and your app will immediately do whatever you have coded it
to do in the `on_login_success` function of the `FirebaseLoginScreen`.

Usage
-

<b>Clone the project</b>

`cd` to your project's directory. Clone this repository using <br>
`git clone https://github.com/Dirk-Sandberg/FirebaseLoginScreen.git`

Which will create a folder named FirebaseLoginScreen in your project.

<h5><b>Update main.kv</b></h5>

In the kv file where you want to use the login screen, include these statements:
<br>

    #:include FirebaseLoginScreen/firebaseloginscreen.kv
    #:import FirebaseLoginScreen FirebaseLoginScreen.firebaseloginscreen.FirebaseLoginScreen

You also need to set the <b>web api key</b> of your Firebase project. This
can be found in your Firebase project by clicking on the settings wheel in the
top left of the Firebase dashboard for your project. Then click 
<b>Project Settings</b>.

Now you can instantiate the FirebaseLoginScreen class, which inherits from the
Kivy `Screen` class. That means you need to add it to your `ScreenManager`.

You should define the `on_login_success` function to execute whatever code you
want once a user has logged in. Probably you'll want to 1) Retrieve some data
from Firebase and 2) switch to a different screen in your `ScreenManager`.

Typically, when making requests to your database to get data for your user, you
identify the user by their `localId`. You can use the `idToken` to authenticate
a user's request to the database if you have set up Firebase <b>Rules</b>. Both
of these variables are automatically retrieved for you by `FirebaseLoginScreen`.<br>
A (fully functional) example of including the proper code in your KV file is
shown in the example below:

`main.kv`
    
    #:include FirebaseLoginScreen/firebaseloginscreen.kv
    #:import FirebaseLoginScreen FirebaseLoginScreen.firebaseloginscreen.FirebaseLoginScreen
    #:import utils kivy.utils
    
    ScreenManager:
        FirebaseLoginScreen:
            id: firebase_login_screen
            name: "firebase_login_screen"
            web_api_key: "your_web_api_key_from_firebase" # Found in Firebase -> Project Settings -> Web API Key
            primary_color: utils.get_color_from_hex("#EE682A")
            secondary_color: utils.get_color_from_hex("#060809")
            tertiary_color: (.25, .25, .25, 1)
            on_login_success:
                # Defining this function lets you program what to do when the
                # user has logged in (probably you'll want to change screens)!
                # Get the important user info
                app.user_localId = self.localId
                app.user_idToken = self.idToken

Make sure the FirebaseLoginScreen is the first screen in your `ScreenManager`.

That's it! Run your app and enjoy your login screen.

##### --------- NOTE: ENABLE EMAIL AUTHENTICATION ---------
Your Firebase project must be allowed to register users through an email and
password. You can set this up easily by going to the Authentication portion of your
Firebase project.

##### --------- NOTE: CUSTOMIZE RESET PASSWORD EMAIL ---------

You can customize the email that is sent to users when they want to reset their email.
Go to your Firebase project, then go to <b>Authentication</b>, then click on <b>Templates</b>,
then click on <b>Password reset</b>

This module makes use of the Progress Spinner widget from the
<a href="https://github.com/kivy-garden/garden.progressspinner" target="_blank">
kivy.garden.progressspinner</a> package. 

Suggestions
-

Add a background image to your login screen to make it much less plain. Do it by
adding an image to the canvas of your `FirebaseLoginScreen` in the kv language.
Example:

    FirebaseLoginScreen:
        canvas.before:
            Rectangle:
                size: self.size
                pos: self.pos
                source: "your/image/here.png"
                
                
If your app takes a long time to start up, you may need to set the `web_api_key`
from python instead of in the kv language. You need to set it in the `on_start`
method of your `App` class. Haven't fully characterized this race condition yet. 



