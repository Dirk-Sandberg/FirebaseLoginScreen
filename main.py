if __name__ == "__main__":
    from kivy.app import App

    # -- This import can be done in kv lang or python

    class MainApp(App):
        login_primary_color = (1, 0, 0)
        login_secondary_color = (1, 1, 0, 1)
        login_tertiary_color = (0,0, 1)
        pass


    MainApp().run()