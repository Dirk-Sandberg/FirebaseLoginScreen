# FirebaseLoginScreen
#### UNDER DEVELOPMENT - UNSTABLE ###
Complete login screen with backend included for Kivy apps

This package lets you very easily incorporate a login screen into your app.

<h2><b>--------- USAGE ---------</b></h1>

In your main.py file, include the following import statement:<br>
`import FirebaseLoginScreen`

Then, in the kv file where you want to use the login screen, include this statement:
<br>`#:include FirebaseLoginScreen/firebaseloginscreen.kv`

Now you can instantiate the FirebaseLoginScreen class, which inherits from the
Kivy Screen class. That means you need to add it to your ScreenManager.

Typically, when making requests to your database to get data for your user, you
identify the user by their `localId`. You can use the `idToken` to authenticate
a user's request to the database if you have set up Firebase <b>Rules</b>. Both
of these variables are automatically retrieved for you by `FirebaseLoginScreen`.<br>
Code Example:<br>
`main.py`

    from kivy.app import App
    
    from FirebaseLoginScreen.firebaseloginscreen import FirebaseLoginScreen
    
    class MainApp(App):
        pass
        
    MainApp().run()



`main.kv`
    
    #:include FirebaseLoginScreen/firebaseloginscreen.kv

    ScreenManager:
        FirebaseLoginScreen:
            id: firebase_login_screen
            secret_api_key: "your_web_api_key_from_firebase" # Found in Firebase -> Project Settings -> Web API Key
            primary_color: (1,0,0)   # Customize the
            secondary_color: (0,1,0) # _ color theme
            tertiary_color: (0,0,1)  # __ of the login screens
            on_login_success: # Meant to be overwritten
                # Get the important user info
                app.user_email = self.email
                app.user_localId = self.localId
                app.user_
                app.do_whatever()  # Your function when they log in


<h5><b>--------- NOTE: ENABLE EMAIL AUTHENTICATION ---------</b></h5>
Your Firebase project must be allowed to register users through an email and
password. You can set this up easily by going to the Authentication portion of your
Firebase project.

<h5><b>--------- NOTE: CUSTOMIZE RESET PASSWORD EMAIL ---------</b></h5>
You can customize the email that is sent to users when they want to reset their email.
Go to your Firebase project, then go to <b>Authentication</b>, then click on <b>Templates</b>,
then click on <b>Password reset</b>


