'''
Created on Feb 16, 2014

@author: Vincent Ketelaars
'''
from threading import Thread, Event
from languages.language import Language
from languages.logger import get_logger
logger = get_logger(__name__)

class Parser(Thread):
    '''
    Parse ISO 639 CSV file
    @note Information from http://stackoverflow.com/a/3218922/1444854
    @note Source http://loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt
    ISO 639-2 Alpha-3 bibliographic code
    ISO 639-2 Alpha-3 terminology code
    ISO 639-1 Alpha-2 code
    English language name(s)
    French language name(s)
    '''

    def __init__(self, filename):
        Thread.__init__(self, name="Parser")
        self.filename = filename
        self.setDaemon(True)
        self._languages = {} # { a3_biblio, Language }
        self._event = Event()
        
    @property
    def languages(self):
        return self._languages
        
    def run(self):
        try:
            for line in open(self.filename, "r"):
                language = self._parse_line(line)
                if language is not None:
                    self._languages[language.alpha_3_bibliographic] = language
        except IOError:
            logger.exception("Could not read %s", self.filename)
        self._event.set()
                    
    def _parse_line(self, line):
        elements = line.split("|")
        if len(elements) != 5:
            logger.warning("Not able to parse %s", line)
            return None
        english = elements[3].split("; ")
        french = elements[4].split("; ")
        return Language(elements[0], elements[1], elements[2], english, french)
    
    def ready(self):
        return not self._event.is_set()
    
    def wait(self, timeout=0.0):
        self._event.wait(timeout)