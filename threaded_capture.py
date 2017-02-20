import threading
import time
from selenium import webdriver
import StringIO
import contextlib
from PIL import Image

class Screenshooter(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.driver_obj = webdriver.PhantomJS

    @contextlib.contextmanager
    def quitting(thing):
        yield thing
        thing.quit()

    def image_name(url):
        name = url.split("//")[-1].split("/")[0]
        name += '_%s.png' % time.time()
        return name

    def save_image(self, driver, url):
        driver.implicitly_wait(10)
        driver.get(url)
        path = self.image_name(url)
        driver.set_window_size(1920, 1080) # optional
        driver.save_screenshot(path)
        # screen = driver.get_screenshot_as_png() 
        # im = Image.open(StringIO.StringIO(screen))
        # im.save('screen_lores.jpg', 'JPEG', optimize=True, quality=95)
        return

    def runner(self, url):
        startTime = time.time()
        with self.quitting(self.driver_obj()) as driver:
            self.save_image(driver, url)
            t = time.time() - startTime
        print "%s: %.3f" % (url, t)


    def run(self):
        """ Method that runs forever """
        for item in range(13951202000207, 13951202000217):
            url = "http://www.farsnews.com/newstext.php?nn=%s" % item
            thread = threading.Thread(target=self.runner, args=(url))
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution

            time.sleep(self.interval)

screen = Screenshooter()
time.sleep(3)
print('Checkpoint')
time.sleep(2)
print('Bye')