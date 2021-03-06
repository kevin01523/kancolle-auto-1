from sikuli import *
from random import uniform
from time import sleep as tsleep, strftime
from re import match

Settings.OcrTextRead = True

# Custom sleep() function to make the sleep period more variable. Maximum
# sleep length is 2 * sec
def sleep(sec):
    tsleep(uniform(sec, sec * 2))

# Custom function to get some pseudo-random value. Here in case variability is
# needed in a non-sleep() function. Maximum return is base + flex.
# value is 2 * integer
def get_rand(base, flex):
    return int(uniform(base, base + flex))

# Custom function to get timer value of Kancolle (in ##:##:## format). Attempts
# to fix values in case OCR grabs the wrong characters.
def check_timer(kc_window, timer_img, width):
    timer_raw = find(timer_img).right(width).text()
    timer = list(timer_raw)
    timer[2] = ':'
    timer[5] = ':'
    timer = ''.join(timer)
    timer = (
        timer.replace('l', '1').replace('I', '1').replace('[', '1').replace(']', '1')
        .replace('|', '1').replace('!', '1').replace('O', '0').replace('o', '0')
        .replace('D', '0').replace('Q', '0').replace('@', '0').replace('S', '5')
        .replace('s', '5').replace('$', '5').replace('B', '8')
    )
    return timer

# Random Click action. Offsets the mouse into a random point within the
# matching image/pattern before clicking.
def rclick(kc_window, pic):
    # This slows down the click actions, but it looks for the pattern and
    # finds the size of the image from the resulting Pattern object.
    m = match(r'M\[\d+\,\d+ (\d+)x(\d+)\]', str(find(pic)))
    if m:
        # If a match is found and the x,y sizes can be ascertained, generate
        # the random offsets. Otherwise, just click the damn middle.
        x_width = int(m.group(1)) / 2
        y_height = int(m.group(2)) / 2
        if isinstance(pic, str):
            pic = Pattern(pic).targetOffset(int(uniform(-x_width, x_width)), int(uniform(-y_height, y_height)))
        elif isinstance(pic, Pattern):
            pic = pic.targetOffset(int(uniform(-x_width, x_width)), int(uniform(-y_height, y_height)))
    kc_window.click(pic)

# common Sikuli actions
def check_and_click(kc_window, pic):
    if kc_window.exists(pic):
        rclick(kc_window, pic)
        #kc_window.click(pic)
        return True
    return False

def wait_and_click(kc_window, pic, time=0):
    if time:
        kc_window.wait(pic, time)
    else:
        kc_window.wait(pic)
    rclick(kc_window, pic)
    #kc_window.click(pic)

# log colors
class color:
    MSG = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

def format(msg):
    now = strftime("%Y-%m-%d %H:%M:%S")
    return "[%s] %s" % (now, msg)

def log_msg(msg):
    print "%s%s%s" % (color.MSG, format(msg), color.END)

def log_success(msg):
    print "%s%s%s" % (color.SUCCESS, format(msg), color.END)

def log_warning(msg):
    print "%s%s%s" % (color.WARNING, format(msg), color.END)

def log_error(msg):
    print "%s%s%s" % (color.ERROR, format(msg), color.END)
