from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock

from PIL import Image
import numpy as np
import os

# https://stackoverflow.com/questions/61185454/kivy-disable-screen-timeout

class CameraRecordButton(ButtonBehavior, Label):
    pass

class CustomProgressBar(Widget):
    pass

class CaptureScreen(Screen):

    # in seconds:
    INTERVAL = 1
    DURATION = 10
    N_IMAGES = int(DURATION / INTERVAL)
    recording = False

    def start_capturing(self):
        if self.recording:
            return
        
        self.images = []
        self.set_recording_status(True)
        self.ids['progress_indicator'].opacity = 1
        self.update_progress_bar()
        self.image_capture_interval = Clock.schedule_interval(self.on_capture_image, self.INTERVAL)

    def on_capture_image(self, dt):
        texture = self.ids['camera'].texture
        size = texture.size
        pixels = texture.pixels
        img = Image.frombytes(mode='RGBA', size=size, data=pixels).convert('L')
        # TODO: use autocrop and resize images

        self.images.append(np.array(img))

        self.update_progress_bar()

        if len(self.images) == self.N_IMAGES:
            self.image_capture_interval.cancel()
            self.set_recording_status(False)
            self.process_images()

    def update_progress_bar(self):
        progress_bar = self.ids['progress_bar']
        progress_text = self.ids['progress_text']
        progress_bar.value = len(self.images) / self.N_IMAGES
        progress_text.text = f"Captured: ({len(self.images)}/{self.N_IMAGES})"

    def set_recording_status(self, status: bool):
        self.ids['record_button'].disabled = self.recording = status

    def process_images(self):
        print([img.shape for img in self.images])
        

class CameraDemoApp(App):
    def build(self):
        return CaptureScreen()

if __name__ == "__main__":
    CameraDemoApp().run()