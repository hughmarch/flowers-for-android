from kivy.app import App
from kivy.uix.image import Image as KvImage
from kivy.uix.screenmanager import Screen

import os

class ResultScreen(Screen):
    def on_pre_enter(self, *args):
        sm = App.get_running_app().root
        self.ids['prediction'].text = sm.statedata.prediction
        self.ids['img'].texture = sm.statedata.capturedImageTexture
        imagesLayout = self.ids['images']
        imagesLayout.clear_widgets()
        path = os.path.join('samples', sm.statedata.prediction)

        files = os.listdir(path)
        for filename in files:
            im = KvImage(source=os.path.join(path, filename))
            im.allow_stretch = True
            imagesLayout.add_widget(im)

        return super().on_pre_enter(*args)