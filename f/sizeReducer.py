from PIL import Image, UnidentifiedImageError
from .side_func import get_new_name
import os
import numpy as np
import random

BASE_DIR = os.getcwd()

def get_filename(path_):
    """ Return a filename of a given filepath """
    t = os.path.split(path_)[-1]
    return t

def get_filename_and_ext(path_):
    """ Return a filename and extention as a tuple of a given path_ """
    a = get_filename(path_)
    t = a.split('.')
    return t[0], t[-1]

class SizeReducer:
    public_f = [
        'all_to_thumbs'
    ]
    def __init__(self, img_url):
        self.img_url = img_url
        self.out_name = get_new_name(img_url)
    

from abc import ABCMeta, abstractmethod, abstractproperty

class AbsImage(metaclass=ABCMeta):
    @abstractproperty
    def get_img(self):
        pass

    @abstractproperty
    def get_path(self):
        pass

    @abstractmethod
    def extend_public(self):
        pass

    @abstractmethod
    def save(self):
        pass

class BaseImage(AbsImage):

    def __init__(self, img:Image, img_path:str):
        self.img = img
        self.img_path = img_path
        self.pub_func = []
        self.extend_public()

    @property
    def get_img(self):
        return self.img

    @property
    def get_path(self):
        return self.img_path

    def extend_public(self):
        self.pub_func.extend([
            'save'
        ])

    def save(self):
        raise NotImplementedError('There is no save method')

    @classmethod
    def from_image_path(cls, img_path:str):
        """ Makes cls instance from image path
            :img_path [str] - absolute path to the image
        """
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            raise OSError('Cannot open the file. Make sure the path contains only latin letters and no spaces')
        except UnidentifiedImageError:
            raise OSError('Cannot open the file. Make sure the path contains only latin letters and no spaces')
        except Image.DecompressionBombError:
            raise Image.DecompressionBombError('Too large image')

        return cls( img=img,
                    img_path=img_path)

class ImageP(BaseImage):
    """ Image class contains all methods to process image colors and size """
    to_thumb = os.path.join(BASE_DIR, 'thumb')
    """ Base path to the thumbnails save directory """
    to_save = os.path.join(BASE_DIR, 'remake')
    """ Base path to the save directory """
    prev_image = None
    """ Link to the previous processed image. Its needed to rollback """
    m_ext = '.png'
    """ Base extention in this class """
    m_filename = None
    """ Modifided filename. (new extention added) """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename_no_ext, self.orig_ext = get_filename_and_ext(self.img_path)
        self.m_filename = self.filename_no_ext + self.m_ext # any formats to png format

    def no_same_filename(self, to_save):
        """ If there is existing file with the same filename make a new filename """
        while os.path.exists(os.path.join(to_save, self.m_filename)):
            rnd = "".join(random.sample("QWERTYUIOPASDFGHJKLZXCVBNM", k=5))
            self.m_filename = self.filename_no_ext + rnd + self.m_ext

    def __sure_save(self):
        if not os.path.exists(self.to_save):
            os.mkdir(self.to_save)

    def __sure_thumb(self):
        if not os.path.exists(self.to_thumb):
            os.mkdir(self.to_thumb)
    
    def extend_public(self):
        super().extend_public()
        self.pub_func.extend([
            'make_thumb',
            'quantize'
        ])

    def quantize(self, colors=256, method=None, kmeans=0, palette=None, dither=1):
        """ Convert the image to ‘P’ - png mode with the specified number of colors. """
        self.prev_image = self.img
        self.img = self.img.quantize(colors, method, kmeans, palette, dither)

    def save(self):
        """ Saves a processed image """
        self.__sure_save()
        self.no_same_filename(self.to_save)
        self.img.save(os.path.join(self.to_save, self.m_filename),
                            format='png', optimized=True)
    
    def make_thumb(self):
        """ Makes a thumbnail of a processed image """
        self.__sure_thumb()
        self.no_same_filename(self.to_thumb)
        a = self.img.copy()
        a.thumbnail(size=(200, 300)) # in place
        a.save(os.path.join(self.to_thumb, self.m_filename),
                format='png', optimized=True)
        print("Thumbnails created")

class ImageB(BaseImage):
    pass
