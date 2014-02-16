'''
Created on Feb 16, 2014

@author: Vincent Ketelaars
'''

class Language(object):
    '''
    Language object containing:
    ISO 639-2 Alpha-3 bibliographic code
    ISO 639-2 Alpha-3 terminology code
    ISO 639-1 Alpha-2 code
    English language name(s)
    French language name(s)
    '''

    def __init__(self, a3_biblio, a3_term, a2, english, french):
        """
        @type a3_biblio: str
        @type a3_term: str
        @type a2: str
        @type english: List(str)
        @type french: List(str)
        """
        self._a3_biblio = a3_biblio
        self._a3_term = a3_term
        self._a2 = a2
        self._english = english
        self._french = french
        
    @classmethod
    def copy(cls, language):
        assert isinstance(language, Language)
        return cls(language._a3_biblio, language._a3_term, language._a2, language._english[:], language._french[:])
        
    @property
    def alpha_3_bibliographic(self):
        return self._a3_biblio
    
    @property
    def alpha_3_terminology(self):
        return self._a3_term
    
    @property
    def alpha_2(self):
        return self._a2
    
    @property
    def languages_en(self):
        return self._english
    
    @property
    def languages_fr(self):
        return self._french
    
    def languages(self, lang="en"):
        if lang == "en":
            return self._english
        elif lang == "fr":
            return self._french
        else:
            return []
        
    def has_acronym(self, acronym):
        if acronym.lower() in [self._a3_biblio, self._a3_term, self._a2]:
            return True
        return False
    
    def __str__(self):
        return "%s|%s|%s|%s|%s" % (self._a3_biblio, self._a3_term, self._a2, "; ".join(self._english), "; ".join(self._french))