from Queue import Queue
from threaded_capture import Screenshooter

def download_fars_news():
    q = Queue()
    for item in range(13951202000207, 13951202000218):
        q.put('http://www.farsnews.com/newstext.php?nn=%s' % item)
    screen = Screenshooter(q)
    q.join()

if __name__ == '__main__':
    download_fars_news()
