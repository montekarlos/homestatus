from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from random import randint
from overview import Overview
from pong import PongGame
import sys 

class MainCarousel(Carousel):
    pongLoopTick = None # Pong animation loop
    game = None # Pong game
    overview = None # Overview panel
    
    def __init__(self):
        # Create carousel - doesn't work so well in .kv
        Carousel.__init__(self,direction='right',loop='true',scroll_distance=80,scroll_timeout=100)
        self.overview = Overview()
        self.add_widget(self.overview)
        self.add_widget(Label(text='Hello World2'))
        self.game = PongGame()
        self.game.serve_ball()
        self.add_widget(self.game)

    def on_index(self, *args):
        slideIndex = args[1]
        print ("slide #{}".format(args[1]))
        if 2 == slideIndex:
            self.pongLoopTick = Clock.schedule_interval(self.game.update, 1.0/60.0)
        elif None != self.pongLoopTick:
            Clock.unschedule(self.pongLoopTick)
            self.pongLookTick = None
        super(MainCarousel, self).on_index(self, args)

class HomeApp(App):
    def build(self):
        # Raspberry 7" resolution test
        Config.set('graphics', 'width', 800)
        Config.set('graphics', 'height', 480)
        app = MainCarousel()
        return app

if __name__ == '__main__':
    #try:
        HomeApp().run()
    #except Exception:
    #    sys.exit(-1)

    
