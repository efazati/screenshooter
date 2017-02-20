#-*- coding: utf-8 -*-
from selenium import webdriver
import StringIO
import contextlib
# from PIL import Image
import time
# export PATH=$PATH:/var/lib/geckodriver
@contextlib.contextmanager
def quitting(thing):
    yield thing
    thing.quit()

def image_name(url):
    name = url.split("//")[-1].split("/")[0]
    name += '_%s.png' % time.time()
    return name

def save_image(driver, url):
    driver.implicitly_wait(10)
    driver.get(url)
    path = image_name(url)
    driver.set_window_size(1920, 1080) # optional
    driver.save_screenshot(path)
    # screen = driver.get_screenshot_as_png() 
    # im = Image.open(StringIO.StringIO(screen))
    # im.save('screen_lores.jpg', 'JPEG', optimize=True, quality=95)
    return

def runner(driver_obj, url):
    startTime = time.time()
    with quitting(driver_obj()) as driver:
        save_image(driver, url)
        t = time.time() - startTime
    print "%s: %.3f" % (driver_obj, t)


url = "http://www.farsnews.com/newstext.php?nn=13951202000207"
#runner(webdriver.Firefox, url)
runner(webdriver.PhantomJS, url)
