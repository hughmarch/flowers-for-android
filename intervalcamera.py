from kivy.lang.builder import Builder
from kivy_garden.xcamera import XCamera
from kivy.uix.camera import Camera
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty

class IntervalCaptureProgressBar(Widget):
    pass

class IntervalCaptureProgressIndicator(BoxLayout):
    def update(self, current, total):
        progress_bar = self.ids['progress_bar']
        progress_text = self.ids['progress_text']
        progress_bar.value = current / total
        progress_text.text = f"Captured: ({current}/{total})"

class IntervalCameraShootButton(ButtonBehavior, Label):
    pass

class IntervalCamera(XCamera):
    """
    IntervalCamera is a Kivy widget that when the record button is pressed, a sequence
    of images is defined by an interval and duration.

    Events:
        `on_capture_image`
            Fired each time the camera captures an image. Passes in arguments (camera,
            texture).
            Example: `on_capture_image: root.do_something(*args)`
        `on_finish`
            Fired once all images have been captured.
    """

    interval = NumericProperty(1)
    """
    Time in seconds the camera should wait before taking the next image.
    """

    duration = NumericProperty(10)
    """
    Time in seconds the camera should take images for. `n_images = duration / interval`.
    """

    _capturing = False

    def __init__(self, **kwargs):
        self.register_event_type('on_capture_image')
        self.register_event_type('on_finish')
        Builder.load_file("./intervalcamera.kv")
        self.force_landscape()
        Camera.__init__(self, **kwargs)

    def shoot(self):
        if self._capturing:
            return
        
        self.n_images = int(self.duration / self.interval)
        self.current = 0
        self.set_capturing_status(True)
        self.ids['progress_indicator'].opacity = 1
        self.update_progress_bar()
        self.image_capture_interval = Clock.schedule_interval(self._on_capture_image, self.interval)

    def _on_capture_image(self, dt):
        texture = self.texture
        self.dispatch('on_capture_image', texture)

        self.current += 1
        self.update_progress_bar()

        if self.current == self.n_images:
            self.image_capture_interval.cancel()
            self.set_capturing_status(False)
            self.dispatch('on_finish')

    def update_progress_bar(self):
        self.ids['progress_indicator'].update(self.current, self.n_images)

    def set_capturing_status(self, status):
        self.ids['camera_button'].disabled = self._capturing = status

    def on_capture_image(self, *args):
        pass

    def on_finish(self):
        pass