from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import platform

from square_camera import SquareCamera
from main_screen import MainScreen
from result_screen import ResultScreen

class AppState(EventDispatcher):
    prediction = StringProperty()
    capturedImageTexture = ObjectProperty()

class StateManager(ScreenManager):
    statedata = ObjectProperty(AppState())

class FlowersApp(App):
    rotated = platform == 'android'

    def build(self):
        sm = StateManager()
        sm.add_widget(MainScreen())
        sm.add_widget(ResultScreen())

        return sm

if __name__ == '__main__':
    if platform == 'android':
        from android.permissions import request_permission, check_permission, Permission
        if not check_permission(Permission.CAMERA):
            request_permission(Permission.CAMERA)
        else:
            FlowersApp().run()

    FlowersApp().run()