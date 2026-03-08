from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen


class RadarApp(MDApp):
    def build(self):
        return MDLabel(
            text="[ NEXUS RADAR ACTIVE ]",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1),
        )


if __name__ == "__main__":
    RadarApp().run()

