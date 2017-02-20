import threading
import signal
import time
from Queue import Queue
from selenium import webdriver
import contextlib
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(threadName)s] %(message)s',
                    datefmt='%H:%M:%S')

class Screenshooter(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, q, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        :type q: Queue
        :param q: queue of urls
        """
        self.interval = interval
        self.driver_obj = webdriver.PhantomJS
        self.q = q
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
            item = self.q.get()
            logger.info("Process %s" % (item))
            self.runner(item)
            self.q.task_done()

    def run(self):
        """ Method that runs for range """
        for i in range(8):
            thread = threading.Thread(target=self.worker, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution

if __name__ == '__main__':
    q = Queue()
    q.put('http://cvas.ir')
    screen = Screenshooter(q)
    q.join()
