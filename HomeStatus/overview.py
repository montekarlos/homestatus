import time
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from filechooserthumbview import FileChooserThumbView
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from config import Config
from solarstatus import SolarStatus
from kivy.utils import strtotuple
from ast import literal_eval as make_tuple

class Overview(Widget):
    current_time = StringProperty("Initialising")
    current_date = StringProperty("Initialising")
    config = Config()
    
    def __init__(self, **kwargs):
        super(Overview, self).__init__(**kwargs)
        self.update_time(0)

        # Setup update loops
        Clock.schedule_interval(self.update_time, 5.0)

        # Load pictures
        picture1 = Picture(photo_config=self.config.photo1_config,
                           config=self.config)
        self.add_widget(picture1, 10)
        picture2 = Picture(photo_config=self.config.photo2_config,
                           config=self.config)
        self.add_widget(picture2, 10)
        solarStatus = SolarStatus(self.config, x=5, y=350)
        self.add_widget(solarStatus)

    def update_time(self, dt):
        self.current_time = time.strftime("%I").strip('0') + time.strftime(":%M %p")
        self.current_date = time.strftime("%d %B")
        #print("Tick: {}".format(self.current_time))

class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''
    source = StringProperty(None)
    touch_down = False
    touch_move = False
    popup_open = False
    imageBrowse = None

    def __init__(self,photo_config,config):
        super(Picture, self).__init__()
        self.photo_config = photo_config
        self.config = config
        self.source = photo_config.path
        self.bind(source=self.set_source)
        self.pos = make_tuple(photo_config.pos)
        self.rotation = float(photo_config.rotation)
        self.scale = float(photo_config.scale)

    def set_source(self, instance, value):
        self.photo_config.path = value

    def on_touch_down(self, touch):
        super(Picture, self).on_touch_down(touch)
        if (self.collide_point(*touch.pos)):
            self.touch_down = True
            #print("Touch down")

    def on_touch_move(self, touch):
        super(Picture, self).on_touch_move(touch)
        if (self.collide_point(*touch.pos)):
            self.touch_move = True
            #print("Touch move")

    def on_touch_up(self, touch):
        super(Picture, self).on_touch_up(touch)
        if (self.collide_point(*touch.pos)):
            #print("Touch up {}".format(self.touch_move))
            if self.touch_move == False and self.popup_open == False and self.touch_down == True:
                print("Choose photo")
                self.popup_open = True
                self.imageBrowse = ImageBrowse(photos_path=self.config.photos_path,thumbs_path=self.config.get_thumbs_path())
                popup = Popup(content=self.imageBrowse,title='Select Image',
                              size_hint=(.8, .8))
                popup.bind(on_dismiss=self.dismiss_callback)
                popup.open()
            self.touch_down = False
            self.touch_move = False
            self.photo_config.pos = str(self.pos)
            self.photo_config.rotation = str(self.rotation)
            self.photo_config.scale = str(self.scale)
            
            
    def dismiss_callback(self, i):
        sel_photo_list = self.imageBrowse.fileChooser.selection
        if sel_photo_list:
            print("Selection: {}".format(sel_photo_list[0]))
            self.source = sel_photo_list[0]
        self.popup_open = False


class ImageBrowse(BoxLayout):
    fileChooser = None
    
    def __init__(self,photos_path,thumbs_path):
        super(ImageBrowse, self).__init__()
        self.orientation = "vertical"
        #self.size_hint = (.9, .85)
        #box = BoxLayout(,size=self.size,pos=self.pos)
        #self.add_widget(box)
        self.fileChooser = FileChooserThumbView(thumbsize=128,size_hint=(1,0.8),thumbdir=thumbs_path,
                                                path=photos_path,rootpath=photos_path)
        #fileChooser = FileChooserIconView(path='C:\\Users\\K\\Pictures\\iCloud Photos\\Downloads')
        self.add_widget(self.fileChooser)
        
