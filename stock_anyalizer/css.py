import yaml
import const 
from PyQt5.QtGui import QFont 


class AnyaStyle():
    def __init__(self):
        with open(const.CSS_FILE) as f:
            self.css = yaml.load(f, Loader=yaml.FullLoader)      

    def GetDefaultFont(self) ->QFont:
        font_family = str(self.css[const.CSS_DEFAULT_FONT_FAMILY])
        font_size = int(self.css[const.CSS_DEFAULT_FONT_SIZE])
        return QFont(font_family,font_size)