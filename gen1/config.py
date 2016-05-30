import configparser
from os.path import expanduser

class Config:
    photos_path = ''
    config_path = '~/.config/homestatus.ini'

    def __init__(self):
        self._photo1_path = ''
        self._photo1_pos = ''
        self._photo2_path = ''
        self._photo2_pos = ''
        self.load()

    def load(self):
        config = configparser.ConfigParser()
        config.read(expanduser(self.config_path))
        if 'photos' in config:
            photos = config['photos']
            self.photos_path = photos.get('photos_path', '')
            self._photo1_path = photos.get('photo1_path', '')
            self._photo1_pos = photos.get('photo1_pos', '')
            self._photo2_path = photos.get('photo2_path', '')
            self._photo2_pos = photos.get('photo2_pos', '')

    def save(self):
        config = configparser.ConfigParser()
        config['photos'] = { 'photos_path': self.photos_path,
                             'photo1_path': self.photo1_path,
                             'photo1_pos': self.photo1_pos,
                             'photo2_path': self.photo2_path,
                             'photo2_pos': self.photo2_pos}
        with open(expanduser(self.config_path), 'w') as configfile:
            config.write(configfile)
# Photo 1
    def set_photo1_path(self, value):
        self.photo1_path = value

    @property
    def photo1_path(self):
        return self._photo1_path

    @photo1_path.setter
    def photo1_path(self, value):
        print('Setting photo1 path {}'.format(value))
        self._photo1_path = value
        self.save()

    def set_photo1_pos(self, value):
        self.photo1_pos = value

    @property
    def photo1_pos(self):
        return self._photo1_pos

    @photo1_pos.setter
    def photo1_pos(self, value):
        print('Setting photo1 pos {}'.format(value))
        self._photo1_pos = value
        self.save()
        

# Photo 2
    def set_photo2_path(self, value):
        self.photo2_path = value
        
    @property
    def photo2_path(self):
        return self._photo2_path

    @photo2_path.setter
    def photo2_path(self, value):
        print('Setting photo2 path {}'.format(value))
        self._photo2_path = value
        self.save()

    def set_photo2_pos(self, value):
        self.photo2_pos = value

    @property
    def photo2_pos(self):
        return self._photo2_pos

    @photo2_pos.setter
    def photo2_pos(self, value):
        print('Setting photo2 pos {}'.format(value))
        self._photo2_pos = value
        self.save()        
