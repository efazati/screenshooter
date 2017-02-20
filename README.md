Screenshooter
============

# Description

screenshot from websites with phantomjs and python

# Installing

You can install Bulkshortify by cloning/forking the repository
and just use it

Installing with the cloned/downloaded code

	git clone https://github.com/efazati/screenshoter.git
	cd screenshoter

Installing latest without cloning

	pip install -e git+git@github.com:efazati/screenshoter.git#egg=screenshoter

#Dependency

	sudo apt-get install phantomjs
	pip install -r requirements

# Usage

Go to directory and just use like this

```
python threaded_capture.py
```

also you can develop with screencapture

```
from Queue import Queue
from threaded_capture import Screenshooter

def download_websites():
    q = Queue()
    q.put('http://bab.ir')
    q.put('http://cvas.ir')
    q.put('http://efazati.org')
    screen = Screenshooter(q)
    q.join()

```
# 


