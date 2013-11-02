import re
import logging
import codecs
from os import listdir
from os.path import isfile, join, isdir

from keywords_base import KeywordFinderBase, KeywordFinderException


class KeywordFinderPython(KeywordFinderBase):
    """ Class for finding text keywords using pure python """
    stopwords_dir = ""

    def __init__(self, stopwords_dir):
        """ You should pass full path to directory containing stopword files """
        if not isdir(stopwords_dir):
            raise KeywordFinderException("Stopwords directory does not exist.")
        else:
            self.stopwords_dir = stopwords_dir

    def _split_text(self, text):
        """ Split text into words also cleaning all non-alphanumeric characters and short words """
        expression = re.compile(ur'[\W_]+', re.UNICODE)
        return [word.lower() for word in expression.sub(u' ', text).split()\
                if len(word)>2]

    def _get_available_languages(self):
        """ Get's available languages by listing stopword files."""
        try:
            files = listdir(self.stopwords_dir)
        except OSError:
            raise KeywordFinderException("Can't list stopwords directory.")

        return [f for f in files if isfile(join(self.stopwords_dir, f)) and f[0]!='.']

    def _get_stopwords(self, language):
        """ Loads stopwords from file. """
        try:
            data = codecs.open(join(self.stopwords_dir, language), encoding='utf-8', mode="r")\
                                                                                            .read()
        except IOError:
            logging.error("Can't read stopwords file for language: %s" % language)
            return set()
        try:
            return set(data.splitlines())
        except AttributeError:
            logging.error("Invalid stopwords file for language: %s" % language)
            return set()

    def detect_language(self, text):
        """ Detect language of text by using stopwords files for comparison.

        Args:
            text: string to perform language detection on
        Returns:
            String containing the name of detected language.
        Raises:
            KeywordFinderException: when stopword files directory is invalid

        """
        language_ratios = {}
        words = set(self._split_text(text))

        for language in self._get_available_languages():
            stopwords = self._get_stopwords(language)
            common_elements = words.intersection(stopwords)
            language_ratios[language] = len(common_elements)

        return max(language_ratios, key=language_ratios.get) if len(language_ratios)>0\
            else self.default_lang

    def get_keywords(self, text, language=None):
        """ Get the list of keywords for passed text.

        Args:
            text: string to extract keywords from
            language: optional language string
        Returns:
            List of keywords.
        Raises:
            KeywordFinderException: when stopword files directory is invalid

        """
        text = unicode(text)
        if language is not None:
            if language not in self._get_available_languages():
                logging.warn("User passed an unsupported language: %s. Falling back to: %s." % \
                                                                    (language, self.default_lang))
                language = self.default_lang
        else:
            language = self.detect_language(text)

        stop_words = self._get_stopwords(language)
        words = [word for word in self._split_text(text) if word not in stop_words]

        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        return self._filter_keywords(word_freq)
