if __name__ == "__main__":
    from kivy.app import App
    from kivy import utils

    # -- This import can be done in kv lang or python

    class MainApp(App):
        login_primary_color = utils.get_color_from_hex("#ABCDEF")#(1, 0, 0, 1)
        login_secondary_color = utils.get_color_from_hex("#060809")#(1, 1, 0, 1)
        login_tertiary_color = utils.get_color_from_hex("#434343")#(0,0, 1, 1)
        pass


    MainApp().run()