import time
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from filechooserthumbview import FileChooserThumbView
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

class Overview(Widget):
    current_time = StringProperty("Initialising")
    picture1 = None;
    
    def __init__(self):
        super(Overview, self).__init__()
        # Setup clock update loop
        Clock.schedule_interval(self.update_time, 1.0)

        # Load pictures
        picture1 = Picture(source='C:\\Users\\K\\Pictures\\iCloud Photos\\Downloads\\IMG_0929.JPG')
        self.add_widget(picture1, 10)

        

    def update_time(self, dt):
        self.current_time = time.strftime("%I").strip('0') + time.strftime(":%M:%S %p")
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

    def on_touch_down(self, touch):
        super(Picture, self).on_touch_down(touch)
        self.touch_down = True
        print("Touch down")

    def on_touch_move(self, touch):
        super(Picture, self).on_touch_move(touch)
        self.touch_move = True
        print("Touch move")

    def on_touch_up(self, touch):
        super(Picture, self).on_touch_up(touch)
        print("Touch up {}".format(self.touch_move))
        if self.touch_move == False and self.popup_open == False and self.touch_down == True:
            print("Choose photo")
            self.popup_open = True
            self.imageBrowse = ImageBrowse()
            popup = Popup(content=self.imageBrowse,title='Select Image',
                          size_hint=(.8, .8))
            popup.bind(on_dismiss=self.dismiss_callback)
            popup.open()
        self.touch_down = False
        self.touch_move = False
            
    def dismiss_callback(self, i):
        print("Selection: {}".format(self.imageBrowse.fileChooser.selection[0]))
        self.source = self.imageBrowse.fileChooser.selection[0]
        self.popup_open = False


class ImageBrowse(BoxLayout):
    fileChooser = None
    
    def __init__(self):
        super(ImageBrowse, self).__init__()
        self.orientation = "vertical"
        #self.size_hint = (.9, .85)
        #box = BoxLayout(,size=self.size,pos=self.pos)
        #self.add_widget(box)
        self.fileChooser = FileChooserThumbView(thumbsize=128,size_hint=(1,0.8),thumbdir='c:\\temp\\thumbs',
                                           path='C:\\Users\\K\\Pictures\\iCloud Photos\\Downloads')
        #fileChooser = FileChooserIconView(path='C:\\Users\\K\\Pictures\\iCloud Photos\\Downloads')
        self.add_widget(self.fileChooser)
        
