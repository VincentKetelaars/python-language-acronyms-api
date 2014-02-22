'''
Created on Feb 16, 2014

@author: Vincent Ketelaars
'''
from parse import Parser
from logger import get_logger
from download import Download
from threading import Thread
from language import Language
logger = get_logger(__name__)

ISO_URL = "http://loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt"
ISO_FILENAME = "iso-639.csv"
PARSER_WAIT = 0.1 # Seconds
DOWNLOAD_WAIT = 10.0 # Seconds

class API(object):
    '''
    API to the languages and acronyms presiding in the CSV file
    '''

    def __init__(self, update=False, callback=None):
        '''
        By default, this API is initialized by reading the CSV languages file
        @param update: Use the most up to date version, which requires http retrieval
        @param callback: Callback function that will be called after update is done (Only when update is True)
        '''
        self._languages = {}
        if update:
            t = Thread(target=self._update, name="Updater", kwargs={"callback" : callback})
            t.start()
        else:
            self._languages = self._parse()
    
    @property
    def languages(self):
        return dict(self._languages)
        
    def number(self):
        return len(self._languages)
    
    def get_language_by_acronym(self, acronym):
        """
        Find Language by acronym
        @rtype: Language
        """
        if acronym.lower() in self._languages.keys():
            return Language.copy(self._languages[acronym.lower()])
        return None
    
    def get_language(self, language):
        """
        Find Language by full language name or acronym
        @rtype: Language
        """
        lang = self.get_language_by_acronym(language)
        if lang is not None:
            return lang
        for lang in self._languages.itervalues():
            for l in lang.languages_en + lang.languages_fr:
                if l.lower() == language.lower():
                    return Language.copy(lang)
                
    def _parse(self):
        parser = Parser(ISO_FILENAME)
        parser.start()
        parser.wait(PARSER_WAIT)
        return parser.languages
        
    def _update(self, callback=None):
        download = Download(ISO_URL, ISO_FILENAME)
        download.start()
        download.wait(DOWNLOAD_WAIT)
        self._languages = self._parse()
        if callback is not None:
            callback(self.languages)

# For testing purposes         
if __name__ == "__main__":
    api = API()