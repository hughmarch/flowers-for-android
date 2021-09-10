from kivy.app import App
from kivy.core.image import Texture
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform

import numpy as np
from PIL import Image
import json

TF_SERVICE_URL = 'http://tf-serving-flowers.herokuapp.com/v1/models/model:predict'
TF_SERVICE_HEADERS = {'content-type': 'application/json'}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        self.img_size = (224, 224)
        with open('labels.json') as f:
            self.labels = json.load(f)

        super(MainScreen, self).__init__(**kwargs)

    def set_waiting_response(self, waiting):
        self.ids['camera'].play = not waiting
        self.ids['predict-btn'].disabled = waiting
        self.ids['predict-btn'].text = 'Awaiting Prediction...' if waiting else 'Predict'

    def predict(self):
        # Capture image
        texture = self.ids['camera'].texture
        size = texture.size
        pixels = texture.pixels
        pil_img = Image.frombytes(mode='RGBA', size=size, data=pixels)

        # Preprocess image
        pil_img = pil_img.convert('RGB').resize(self.img_size, resample=Image.BILINEAR)
        if platform == 'android':
            pil_img = pil_img.rotate(-90)
        
        img = np.array(pil_img).astype(np.float32)
        # from imagenet_utils.preprocess_input(), scales values between -1 and 1 for mobilenet
        img /= 127.5
        img -= 1
        img = img.reshape((1, 224, 224, 3))

        def handle_success(request, result):
            yh = np.array(result['predictions'])
            prediction = self.labels[str(np.argmax(yh, axis=1)[0])]
            
            # Send captured image and prediction to the results screen
            sm = App.get_running_app().root
            captureTexture = Texture.create(size=texture.size)
            captureTexture.blit_buffer(pixels, colorfmt='rgba', bufferfmt='ubyte')
            captureTexture.flip_vertical()
            sm.statedata.capturedImageTexture = captureTexture

            sm.statedata.prediction = prediction
            sm.current = 'resultScreen'
            self.set_waiting_response(False)

        def handle_error(request, error):
            print(error)
            self.set_waiting_response(False)

        data = json.dumps({'signature_name': 'serving_default', 'instances': img.tolist()})
        
        UrlRequest(
            TF_SERVICE_URL,
            req_headers=TF_SERVICE_HEADERS,
            req_body=data,
            method='POST',
            on_success=handle_success,
            on_error=handle_error,
            on_failure=handle_error)
        
        self.set_waiting_response(True)