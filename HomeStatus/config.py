import configparser
from os.path import expanduser
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

class PhotoConfig(EventDispatcher):
    path = StringProperty('')
    pos = StringProperty('0, 0')
    scale = StringProperty('1')
    rotation = StringProperty('0')

    def __init__(self, parent, section_name):
        self.inload = True
        self.parent = parent
        self.section_name = section_name;
        self.bind(path=self.save)
        self.bind(pos=self.save)
        self.bind(scale=self.save)
        self.bind(rotation=self.save)

    def load(self, config):
        self.inload = True
        if self.section_name in config:
            section = config[self.section_name]
            self.path = section.get('path')
            self.pos = section.get('pos')
            self.scale = section.get('scale')
            self.rotation = section.get('rotation')
        self.inload = False

    def set_section(self, config):
        config[self.section_name] = { 'path' : self.path,
                                      'pos' : self.pos,
                                      'scale' : self.scale,
                                      'rotation' : self.rotation }

    def save(self, instance, value):
        if not self.inload:
            self.parent.save()

class Config:
    photos_path = ''
    config_path = '~/.config/homestatus.ini'
    thumbs_path = '~/.config/thumbs'

    has_pi_screen = False
    screen_brightness = 80
    switch_off_time = 60

    inverter_ip = '127.0.0.1'


    _SOLAR_SECTION = 'solar'
    _GENERAL_SECTION = 'general'

    def get_thumbs_path(self):
        return expanduser(self.thumbs_path)

    def __init__(self):
        self.photo1_config = PhotoConfig(self, 'photo_1')
        self.photo2_config = PhotoConfig(self, 'photo_2')
        self.load()

    def load(self):
        config = configparser.ConfigParser()
        config.read(expanduser(self.config_path))
        if 'photos' in config:
            photos = config['photos']
            self.photos_path = photos.get('photos_path')
            self.thumbs_path = photos.get('thumbs_path')
        if self._GENERAL_SECTION in config:
            general = config[self._GENERAL_SECTION]
            self.has_pi_screen = general.get('has_pi_screen') in ['1', 'true', 'True', 'y']
            self.screen_brightness = general.get('screen_brightness')
            self.switch_off_time = general.get('switch_off_time')
        if self._SOLAR_SECTION in config:
            solar = config[self._SOLAR_SECTION]
            self.inverter_ip = solar.get('inverter_ip')
        self.photo1_config.load(config)
        self.photo2_config.load(config)

    def save(self):
        config = configparser.ConfigParser()
        config['photos'] = { 'photos_path': self.photos_path,
                             'thumbs_path': self.thumbs_path }
        config[self._GENERAL_SECTION] = { 'has_pi_screen': self.has_pi_screen,
                                          'screen_brightness' : self.screen_brightness,
                                          'switch_off_time' : self.switch_off_time }
        config[self._SOLAR_SECTION] = { 'inverter_ip': self.inverter_ip }
        self.photo1_config.set_section(config);
        self.photo2_config.set_section(config);
        with open(expanduser(self.config_path), 'w') as configfile:
            config.write(configfile)
