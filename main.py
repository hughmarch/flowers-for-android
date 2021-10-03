from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager

from PIL import Image
import numpy as np

class CaptureScreen(Screen):
    images_list = []

    def on_capture_image(self, camera, texture):
        size = texture.size
        pixels = texture.pixels
        img = Image.frombytes(mode='RGBA', size=size, data=pixels).convert('L')
        self.images_list.append(np.array(img))

    def on_finish(self):
        print([img.shape for img in self.images_list])
        self.images_list = []

class CameraDemoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CaptureScreen())
        return sm

if __name__ == "__main__":
        CameraDemoApp().run()