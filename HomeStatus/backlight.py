from kivy.clock import Clock

class RpBacklight:
    brightness_path = "/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness"
    power_path = "/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power"
    max_brightness_path = "/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/max_brightness"

    def __init__(self):
        with open(self.max_brightness_path, mode='r') as f:
            self.max_brightness = float(f.readline());

    def switch_on(self):
        print("Switching on backlight")
        with open(self.power_path, 'wt') as f:
            f.write("0\n") # 0 to swith on

    def switch_off(self):
        print("Switching off backlight")
        with open(self.power_path, 'wt') as f:
            f.write("1\n") # 1 to swith off

    def set_brightness(self, value):
        print("Setting backlight to {}".format(value))
        with open(self.brightness_path, 'wt') as f:
            f.write(str(int(float(value) / 100.0 * self.max_brightness))+ "\n")

class FakeBacklight:
    def switch_on(self):
        print("Switch on backlight")

    def switch_off(self):
        print("Switch off backlight")

    def set_brightness(self, value):
        print("Set brightness to {}%".format(value))

class Backlight:
    step_size = 1.5
    fade_interval = .04

    def __init__(self, config, backlight_hw):
        self.brightness = float(config.screen_brightness)
        self.backlight_hw = backlight_hw
        self.current_brightness = self.brightness
        self.backlight_hw.set_brightness(self.brightness)
        self.backlight_hw.switch_on()

    def fade_in(self):
        Clock.unschedule(self.on_fade_in)
        Clock.unschedule(self.on_fade_out)
        self.backlight_hw.switch_on()
        Clock.schedule_once(self.on_fade_in, self.fade_interval)

    def on_fade_in(self, dt):
        if (self.current_brightness < self.brightness):
            self.current_brightness = self.current_brightness + self.step_size
            self.backlight_hw.set_brightness(self.current_brightness)
            Clock.schedule_once(self.on_fade_in, self.fade_interval)

    def fade_out(self):
        Clock.unschedule(self.on_fade_in)
        Clock.unschedule(self.on_fade_out)
        Clock.schedule_once(self.on_fade_out, self.fade_interval)

    def on_fade_out(self, dt):
        if (self.current_brightness - self.step_size > 0):
            self.current_brightness = self.current_brightness - self.step_size
            self.backlight_hw.set_brightness(self.current_brightness)
            Clock.schedule_once(self.on_fade_out, self.fade_interval)
        else:
            self.backlight_hw.switch_off()

class BacklightFactory:
    @staticmethod
    def Make(config):
        if config.has_pi_screen:
            print("Creating RpBacklight")
            return Backlight(config, RpBacklight())
        else:
            print("Creating FakeBacklight")
            return Backlight(config, FakeBacklight())
