from PIL import Image


def lower_size(img_url):
    print("Optimize image")
    foo = Image.open(img_url)
    # foo = foo.resize((160,300),Image.ANTIALIAS)
    foo.save(img_url,optimize=True,quality=75)
    print("Optimized")
