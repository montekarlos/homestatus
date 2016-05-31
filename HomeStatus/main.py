from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from random import randint
from overview import Overview
from pong import PongGame
from subprocess import call
import sys 
import time

class MainCarousel(Carousel):
    pongLoopTick = None # Pong animation loop
    game = None # Pong game
    overview = None # Overview panel
    
    def __init__(self):
        # Create carousel - doesn't work so well in .kv
        Carousel.__init__(self,direction='right',loop='true',scroll_distance=80,scroll_timeout=100)
        call("echo 150 > /sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness", shell=True)
        call("echo 0 > /sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power", shell=True)
        self.overview = Overview()
        self.add_widget(self.overview)
        self.add_widget(Label(text='Hello World2'))
        self.game = PongGame()
        self.game.serve_ball()
        self.add_widget(self.game)
        self.idle_clock = Clock.schedule_once(self.on_idle, 10)
        Window.bind(on_motion=self.on_motion)

    # Setup screen saver
    def on_motion(self, *args):
        # Switch back light back on 
        print("On Motion")
        self.idle_clock.cancel()
        call("echo 150 > /sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness", shell=True)
        call("echo 0 > /sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power", shell=True)
        self.idle_clock = Clock.schedule_once(self.on_idle, 10)

    def on_idle(self, dt):
        # Switch off back light power
        print("On Idle")
        #for bright in range(150, 0, -1):
        #    call("echo " + str(bright) + " > /sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness", shell=True)
        #    time.sleep(.50)
        call("echo 1 > /sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power", shell=True)

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
