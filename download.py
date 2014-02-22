'''
Created on Feb 16, 2014

@author: Vincent Ketelaars
'''
from threading import Thread, Event
from urllib2 import build_opener, HTTPErrorProcessor, HTTPHandler,\
    HTTPRedirectHandler
from logger import get_logger
logger = get_logger(__name__)

class Download(Thread):
    '''
    Download most current version of ISO file
    '''


    def __init__(self, url, filename):
        '''
        @param url: URL string
        @param filename: Filename string
        '''
        Thread.__init__(self, name="Downloader")
        self.url = url
        self.filename = filename
        self._event = Event()
        self._success = False
        
    def run(self):
        try:
            opener = build_opener(HTTPHandler(), HTTPErrorProcessor(), HTTPRedirectHandler())
            opener.addheaders = [('User-agent', 'Mozilla/5.0')] # Spoof User agent
            response = opener.open(self.url)
            if response.getcode() == 200:
                with open(self.filename, "wb") as f:
                    f.write(response.read())
                    self._success = True
        except: # Not listing each and every exception
            logger.exception("Could not download %s to %s", self.url, self.filename)
        self._event.set()
        
    def ready(self):
        return not self._event.is_set()
    
    def success(self):
        return self._success

    def wait(self, timeout=0.0):
        self._event.wait(timeout)
        