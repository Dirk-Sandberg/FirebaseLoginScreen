from kivymd.app import MDApp

class MainApp(MDApp):
    user_idToken = ""
    local_id = ""

    def display_user_tokens(self):
        self.root.ids.the_label.text = "local_id: " + self.local_id + "\n user_idToken: " + self.user_idToken

    def sign_out(self):
        self.root.ids.firebase_login_screen.log_out()
        self.root.current = 'firebase_login_screen'

MainApp().run()

