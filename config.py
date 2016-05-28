import configparser
from os.path import expanduser

class Config:
    photos_path = ''
    photo1_path = ''
    config_path = '~/.config/homestatus.ini'

    def __init__(self):
        self.load()

    def load(self):
        config = configparser.ConfigParser()
        config.read(expanduser(self.config_path))
        if 'photos' in config:
            photos = config['photos']
            self.photos_path = photos.get('photos_path', '')
            self.photo1_path = photos.get('photo1_path', '')

    def save(self):
        config = configparser.ConfigParser()
        config['photos']['photos_path'] = self.photos_path
        config['photos1']['photo1_path'] = self.photo1_path
        with open(expanduser(self.config_path), 'w') as configfile:
            config.write(configfile)
