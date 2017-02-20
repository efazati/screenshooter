#-*- coding: utf-8 -*-
import unittest
from selenium import webdriver
import time


class Benchmark(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def test_url_fire(self):
        time.sleep(2)
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.farsnews.com/newstext.php?nn=13951202000207") # url associated with date click
        date = self.driver.find_element_by_css_selector("#4743167 .sentCommentsItemDT").get_attribute("value")
        self.assertEquals(u'۰۹:۴۰ دوشنبه ۲ اسفند ۱۳۹۵', date)

    def test_url_phantom(self):
        time.sleep(1)
        self.driver = webdriver.PhantomJS()
        self.driver.get("http://www.farsnews.com/newstext.php?nn=13951202000207") # url associated with date click
        print "4444", self.driver.find_element_by_css_selector("#4743167 .sentCommentsItemDT")
        date = self.driver.find_element_by_css_selector("#4743167.sentCommentsItemDT").get_attribute("value")
        print date
        self.assertEquals(u'۰۹:۴۰ دوشنبه ۲ اسفند ۱۳۹۵', date)

    def tearDown(self):
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Benchmark)
    unittest.TextTestRunner(verbosity=0).run(suite)