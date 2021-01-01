# Finding your Firebase project's Web API Key
You need to pass the web API key to your `FirebaseLoginScreen` widget when you instantiate it. To find your web API key, Click on the Settings cog icon in the top left of your Firebase project. Click on *Project Settings*. You will see your Web API Key in the center of the screen. *According to https://stackoverflow.com/questions/37482366/is-it-safe-to-expose-firebase-apikey-to-the-public/37484053#37484053, It is safe to include this API key in your client-side code.*

# Enabling Email Authentication
On the left navigation menu, click on *Authentication*. Click the big blue *Set up sign-in method* button. Click on *Email*, then enable the first option, and click the *Save* button. That's it!

# Customize the password reset email 
You can customize the email that is sent to users when they want to reset their email.
Go to your Firebase project, then go to <b>Authentication</b>, then click on <b>Templates</b>,
then click on <b>Password reset</b>
