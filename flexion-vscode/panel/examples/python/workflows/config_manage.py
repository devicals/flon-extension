from interpreter import flon

class Config:
    def __init__(self, file):
        flon.load(file)
        self.data = flon.get('root/config')
    
    def get(self, key, default=None):
        return self.data.get(key, default)

config = Config('app.flon')
debug = config.get('debug', False)