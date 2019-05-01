"""
This package lets you very easily incorporate a login screen into your app.

--------- USAGE ---------

In your main.py file, include the following import statement:
import FirebaseLoginScreen

Then, in the kv file where you want to use the login screen, include this statement:
#:include FirebaseLoginScreen/firebaseloginscreen.kv

Now you can instantiate the FirebaseLoginScreen class, which inherits from the
Kivy Screen class. That means you need to add it to your ScreenManager.

Example:
    `main.kv`
    ScreenManager:
        FirebaseLoginScreen:
            id: firebase_login_screen
            web_addr: "gweomg-wewegw"
            secret_api_key: "wkgmwanrg"
            on_login_success:
                app.do_whatever()  # Your function when they log in


--------- NOTE ---------
Your Firebase project must be allowed to register user's through an email and
password. You can allow this by going to the Authentication portion of your
Firebase project.

"""