import threading
import time
from Queue import Queue
from selenium import webdriver
import StringIO
import contextlib
from PIL import Image
import signal
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(threadName)s] %(message)s',
                    datefmt='%H:%M:%S')

q = Queue()

class Screenshooter(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, urls, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.driver_obj = webdriver.PhantomJS
        self.urls = urls
        self.run()

    @contextlib.contextmanager
    def quitting(self, driver):
        yield driver
        driver.service.process.send_signal(signal.SIGTERM) 
        driver.quit()

    def image_name(self, url):
        name = url.split("//")[-1].split("/")[0]
        name += '_%s.png' % time.time()
        return name

    def save_image(self, driver, url):
        driver.implicitly_wait(10)
        driver.get(url)
        path = self.image_name(url)
        logger.info('Download %s as %s' % (url, path))
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
        logger.info("Finished Time %s: %.3f" % (url, t))
        time.sleep(self.interval)


    def worker(self):
        while True:
            item = q.get()
            logger.info("Process %s" % (item))
            self.runner(item)
            q.task_done()

    def run(self):
        """ Method that runs for range """
        for i in range(8):
            thread = threading.Thread(target=self.worker, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution

if __name__ == '__main__':
    urls = []
    for item in range(13951202000207, 13951202000218):
        q.put('http://www.farsnews.com/newstext.php?nn=%s' % item)
    screen = Screenshooter(urls)
    signal.pause()
    q.join()