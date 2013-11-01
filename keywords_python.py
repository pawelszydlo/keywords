import re
from os import listdir
from os.path import isfile, join

from keywords_base import KeywordFinderBase


class KeywordFinderPython(KeywordFinderBase):
    """ Class for finding text keywords using pure python """
    nltk_stopwords_dir = "/Users/widget/nltk_data/corpora/stopwords"
                            # if available - use stopwords from NLTK library

    def _split_text(self, text):
        """ Split text into words also cleaning all non-alphanumeric characters and short words """
        expression = re.compile(ur'[\W_]+', re.UNICODE)
        return [word.lower() for word in expression.sub(u' ', text.decode('utf-8')).split()\
                if len(word)>2]

    def _get_available_languages(self):
        """ Get's available languages by listing stopword files."""
        try:
            files = listdir(self.nltk_stopwords_dir)
        except OSError:
            return []
        return [f for f in files if isfile(join(self.nltk_stopwords_dir, f)) and f[0]!='.']

    def _get_stopwords(self, language):
        """ Loads stopwords from file. """
        try:
            data = open(join(self.nltk_stopwords_dir, language),"r").read()
        except IOError:
            return set()
        try:
            return set(data.splitlines())
        except AttributeError:
            return set()

    def detect_language(self, text):
        """ Detect language of text by using nltk's stopwords for comparison. """
        language_ratios = {}
        words = set(self._split_text(text))

        for language in self._get_available_languages():
            stopwords = self._get_stopwords(language)
            common_elements = words.intersection(stopwords)
            language_ratios[language] = len(common_elements)

        return max(language_ratios, key=language_ratios.get) if len(language_ratios)>0\
            else self.default_lang

    def get_keywords(self, text, language=None):
        """ Get the list of keywords for passed text. """
        if language is not None:
            if language not in self._get_available_languages():
                language = self.default_lang
        else:
            language = self.detect_language(text)

        stop_words = self._get_stopwords(language)
        words = [word for word in self._split_text(text) if word not in stop_words]

        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        return self._filter_keywords(word_freq)
