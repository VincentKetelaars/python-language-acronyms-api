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

    def __init__(self, a3_biblio, a3_term, a2, english, french, encoding):
        """
        @type a3_biblio: unicode
        @type a3_term: unicode
        @type a2: unicode
        @type english: List(unicode)
        @type french: List(unicode)
        @param encoding: Encoding of the parameters
        """
        self._a3_biblio = a3_biblio
        self._a3_term = a3_term
        self._a2 = a2
        self._english = english
        self._french = french
        self._encoding = encoding
        
    @classmethod
    def copy(cls, language):
        assert isinstance(language, Language)
        return cls(language._a3_biblio, language._a3_term, language._a2, language._english[:], language._french[:], language._encoding)
        
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
        
    def acronyms(self):
        a = [self._a3_biblio]
        if len(self._a3_term):
            a.append(self._a3_term)
        if len(self._a2):
            a.append(self._a2)
        return a
        
    def has_acronym(self, acronym):
        if acronym.lower() in self.acronyms():
            return True
        return False
    
    def __str__(self):
        def enc(s):
            if self._encoding is not None:
                return s.encode(self._encoding)
            return s
        
        return "%s|%s|%s|%s|%s" % (enc(self._a3_biblio), enc(self._a3_term), enc(self._a2), 
                                   enc(enc("; ").join(self._english)), enc(enc("; ").join(self._french)))
    
    def __eq__(self, other):
        return self._a3_biblio == other._a3_biblio
    
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self._a3_biblio)