from kivy.clock import Clock

class RpBacklight:
    brightness_path = "/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness"
    power_path = "/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power"
    max_brightness_path = "/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/max_brightness"

    def __init__(self):
        with open(self.max_brightness_path, mode='r') as f:
            self.max_brightness = int(f.readline());
        self.set_brightness(150)
        self.switch_on()

    def switch_on(self):
        with open(self.power_path, mode='a') as f:
            f.writelines("0") # 0 to swith on

    def switch_off(self):
        with open(self.power_path, mode='a') as f:
            f.writelines("1") # 1 to swith on

    def set_brightness(self, value):
        with open(self.brightness_path, mode='a') as f:
            f.writelines(str(value / 100.0 * self.max_brightness))

class FakeBacklight:
    def switch_on(self):
        print("Switch on backlight")

    def switch_off(self):
        print("Switch off backlight")

    def set_brightness(self, value):
        print("Set brightness to {}%".format(value))

class Backlight:
    step_size = 2
    fade_interval = .03

    def __init__(self, config, backlight_hw):
        self.brightness = config.screen_brightness
        self.backlight_hw = backlight_hw
        self.current_brightness = self.brightness
        self.backlight_hw.set_brightness(self.brightness)
        self.backlight_hw.switch_on()

    def fade_in(self):
        Clock.unschedule(self.on_fade_in)
        Clock.unschedule(self.on_fade_out)
        Clock.schedule_once(self.on_fade_in, self.fade_interval)

    def on_fade_in(self, dt):
        if (self.current_brightness <= 0):
            self.backlight_hw.switch_on()

        if (self.current_brightness < self.brightness):
            self.current_brightness = self.current_brightness + self.step_size
            self.backlight_hw.set_brightness(self.current_brightness)
            Clock.schedule_once(self.on_fade_in, self.fade_interval)

    def fade_out(self):
        Clock.unschedule(self.on_fade_in)
        Clock.unschedule(self.on_fade_out)
        Clock.schedule_once(self.on_fade_out, self.fade_interval)

    def on_fade_out(self, dt):
        if (self.current_brightness > 0):
            self.current_brightness = self.current_brightness - self.step_size
            self.backlight_hw.set_brightness(self.current_brightness)
            Clock.schedule_once(self.on_fade_out, self.fade_interval)
        elif (self.current_brightness <= 0):
            self.backlight_hw.switch_off()

class BacklightFactory:
    @staticmethod
    def Make(config):
        if config.has_pi_screen:
            return Backlight(config, RpBacklight())
        else:
            return Backlight(config, FakeBacklight())