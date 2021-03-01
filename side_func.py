import os


def get_str_time(seconds):
    mm = seconds // 60
    ss = seconds % 60
    ss = ss if ss > 9 else f"0{ss}"
    return f"{mm}:{ss}min"

def estimate_time(tt: float, current: int, whole:int, msg:str):
    """ Prints inline message and estimation time to finish
        :tt - time of a processing 1 row
        :current - current row index
        :whole - height of array, number of rows
        :msg - message to show with estimation time
    """
    path = (whole - current)
    est_time = round(path * tt)
    str_time = get_str_time(est_time)
    print(f"{msg} time left: {str_time}", end='')
    print('\r', end='')

def inline_print(msg):
    print(msg, end='')
    print('\r', end='')

def inline_printed(f):
    def wrap(*args, **kwargs):
        res = f(*args, **kwargs)
        print()
        return res
    return wrap 

def get_new_name(img_url, name=''):
    path, img_name = os.path.split(img_url)
    img_name = img_name.split('.')[0]
    if name:
        img_name = name
    out_name = os.path.join(path, f"{img_name}-remake.jpg")
    return out_name