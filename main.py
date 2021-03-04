from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
import os
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scatterlayout import ScatterLayout
from f.sizeReducer import ImageP


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SystemToolbarLayout(AnchorLayout):
    anchor_x = "left"
    anchor_y = "center"

class SystemToolbar(BoxLayout):
    def a(self):
        print('Не трогай меня')

class SystemToolbarItem(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = 30

class ImageToolBarLayout(AnchorLayout):
    anchor_x = "right"
    anchor_y = "center"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class ImageToolbar(BoxLayout):
    pass

class ImageToolbarItem(AnchorLayout):
    anchor_x = "center"
    anchor_y = "center"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50

class ImagePreview(AnchorLayout):
    anchor_x = "center"
    anchor_y = "center"

class TopCenterLayout(BoxLayout):
    anchor_x = "center"
    anchor_y = "top"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))

class CenteredAnchorLayout(AnchorLayout):
    anchor_x = "center"
    anchor_y = "center"
    
class MyApp(MDApp):
    def build(self):
        Window.maximize()
        Window.clearcolor = (.2,.2,.2,1)
        self.root = Builder.load_file(os.path.join(BASE_DIR, 'gui', 'main.kv'))

# MyApp = MyApp()
# MyApp.run()

a = ImageP.from_image_path(r'D:\Python_work\image_procecssing\0001-001-.jpg')
a.quantize(colors=5)
a.save()
