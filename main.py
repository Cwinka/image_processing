import cv2
import numpy as np 
from typing import Union, Tuple
import os
import sys
import time
from side_func import (
    inline_print,
    inline_printed,
    estimate_time,
    get_new_name,
)
    
class Node:
    def __init__(self, color):
        self.color = color

    @property
    def value(self):
        return self.color
    
    def __repr__(self):
        return str(self.color)

class BaseImageGraph:
    def __init__(self, img_url: str, nody_img: np.ndarray, graph_img: dict=None, factor=1):
        if type(nody_img) != np.ndarray:
            raise TypeError('Instance needs to be ndarray')
        # self.graph_img = graph_img
        self.nody_img = nody_img
        self.img_url = img_url
        self.factor = factor

    @classmethod
    def from_cv2_image(cls, img_url, img, factor):
        if type(img) != np.ndarray:
            raise TypeError('Instance of img needs to be ndarray')
        return cls(img_url=img_url,
                   nody_img=img,
                #    graph_img=cls.wrap_with_nodes(img),
                   factor=factor)

    @classmethod
    def from_image_url(cls, img_url, factor):
        img = cv2.imread(img_url)
        return cls(img_url=img_url,
                   nody_img=img,
                #    graph_img=cls.wrap_with_nodes(img),
                   factor=factor)

    @staticmethod
    @inline_printed
    def wrap_with_nodes(img) -> dict:
        """ Make ndarray object with Nodes iside
            :img [ndarray] - readed image by cv2 (by default)
        """
        height = img.shape[0]
        width = img.shape[1]
        graph_img = {}
        for y in range(height):
            s = int(y/height*100)
            msg = f"Writing {s+1}%/{100}%"
            inline_print(msg)
            for x in range(width):
                graph_img[y, x] = Node(img[y,x])
        del img
        return graph_img

    def update(self, y, x, color):
        self.nody_img[y, x] = color
        # self.graph_img[y, x] = color
    
    def save(self, name=''):
        out_name = get_new_name(self.img_url)
        cv2.imwrite(out_name, self.nody_img)
        print(f"Saved")
        return out_name

    def strait_line(self, from_: Tuple[int, int], to: Tuple[int, int], color: Union[list, int]):
        f_y,f_x = from_
        t_y, t_x = to
        if f_y > t_y:
            f_y, t_y = t_y, f_y # if move from right to left
        if f_x > t_x:
            f_x, t_x = t_x, f_x
        if t_y == f_y or t_x == f_x:
            for y in range(f_y, t_y+1):
                for x in range(f_x, t_x+1):
                    self.update(y,x, color)
        else:
            raise ArithmeticError('Not a strait line present')
    
    def square(self, from_: Tuple[int, int], to: Tuple[int, int], color: Union[list, int]):
        f_y,f_x = from_
        t_y, t_x = to
        self.strait_line(from_, (f_y, t_x), [125, 255, 0])
        self.strait_line((f_y, t_x), to, [125, 255, 0])
        self.strait_line(to, (t_y, f_x), [125, 255, 0])
        self.strait_line((t_y, f_x), from_, [125, 255, 0])

    def run_then_get_time(self, f, args):
        """ Measure runtime of a function. Returns (time, result) """
        start = time.perf_counter()
        res = f(*args)
        t_spent = time.perf_counter() - start
        return t_spent, res

    def __repr__(self):
        return str(self.nody_img)
    
    def __getitem__(self, item):
        return self.nody_img[item]
    
class ImageGraph(BaseImageGraph):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = self.nody_img.shape[0]
        self.width = self.nody_img.shape[1]
    
    def __factorize(self, single_color: Union[int, float]) -> int:
        """ Turns color into new one according to the factor """
        res = int(round(self.factor * single_color / 255) * (255/self.factor))
        return res

    def __sure(self, color: Union[float, int, list]) -> Union[list, float, int]:
        """ Prevent color be more than 255 or less than 0 """
        if type(color) != float:
            n = []
            for pix in color:
                pix = 0 if pix < 0 else pix
                pix = 255 if pix > 255 else pix
                n.append(pix)
            color = n
        else:
            color = 0 if color < 0 else color
            color = 255 if color > 255 else color
        
        return color

    @inline_printed
    def to_gray(self):
        """ Make image gray
            :negative [int] - If true, the image will be gray negative
        """
        for y in range(self.height):
            s = int(y/self.height*100)
            msg = f"Perform to gray {s+1}%/100%"
            inline_print(msg)
            for x in range(self.width):
                color = self.nody_img[y, x]
                gray_color = sum(color) / 3
                self.update(y, x, gray_color)

    @inline_printed
    def dither(self):
        """ Make image gray
            :factor [int] - If 1, then all the colors will be changed to pure
            if 2 or more, spectrs of colors will be added
        """
        tt = 0 # current time spent by row
        for y in range(self.height):
            s = int(y/self.height*100)
            msg = f"Dither rgb lay {s+1}%/100%"
            for x in range(self.width):
                sp, _ = self.run_then_get_time(self.__dither_do, args=(y, x))
                tt += sp # accumulate time in row
            estimate_time(  tt=tt,
                            current=y,
                            whole=self.height,
                            msg=msg)
            tt = 0 # clear time

    @inline_printed
    def dither_gray(self):
        """ Make image gray
            :factor [int] - If 1, then all the colors will be changed to pure
            if 2 or more, spectrs of colors will be added
        """
        self.to_gray()
        tt = 0
        for y in range(self.height):
            msg = f"Dither gray lay {y}/{self.height}"
            for x in range(self.width):
                sp, _ = self.run_then_get_time(self.__dither_do, args=(y, x))
                tt += sp # accumulate time in row
            estimate_time(  tt=tt,
                            current=y,
                            whole=self.height,
                            msg=msg)
            tt = 0
    
    def __dither_do(self, y:int, x:int):
        """ Do dither on [y, x] pixel"""
        colors = self.nody_img[y, x]
        new_color = np.array(list(map(lambda color: self.__factorize(color), colors)))
        self.update(y, x, new_color)
        quant_error = colors - new_color

        if (x<self.width-1):
            new_c = self.nody_img[y, x+1] + quant_error * 7/16
            self.update(y, x+1, self.__sure(new_c))
        if (x>0 and y<self.height-1):
            new_c = self.nody_img[y+1, x-1] + quant_error * 3/16
            self.update(y+1, x-1, self.__sure(new_c))
        if (y<self.height-1):
            new_c = self.nody_img[y+1, x] + quant_error * 5/16
            self.update(y+1, x, self.__sure(new_c))
        if (y<self.height-1 and x<self.width-1):
            new_c = self.nody_img[y+1, x+1] + quant_error * 1/16
            self.update(y+1, x+1, self.__sure(new_c))

