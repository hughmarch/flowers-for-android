from kivy.uix.camera import Camera
from kivy.graphics.texture import TextureRegion

class SquareCamera(Camera):
    initialized = False

    def on_texture(self, var, value):
        if not self.initialized:
            self.initialized = True

            # Crop camera texture to largest centered square
            crop_size = min(self.texture.width, self.texture.height)
            self.texture = TextureRegion(
                (self.texture.width - crop_size) // 2, 
                (self.texture.height - crop_size) // 2, 
                crop_size, 
                crop_size, 
                self.texture)