from PIL import Image
from side_func import get_new_name


class SizeReducer:
    def __init__(self, img_url):
        self.img_url = img_url
        self.out_name = get_new_name(img_url)

    def lower_size(self):
        print("Optimize image")
        try:
            foo = Image.open(self.out_name)
        except FileNotFoundError:
            print("To lower image size you need first to save it")
            return
        # foo = foo.resize((160,300),Image.ANTIALIAS)
        foo.save(self.out_name, optimize=True,quality=75)
        print("Optimized")
