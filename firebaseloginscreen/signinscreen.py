from kivy.uix.screenmanager import Screen, SlideTransition

class SignInScreen(Screen):
    def go_back(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "welcome_screen"
        self.parent.transition = SlideTransition(direction="left")

