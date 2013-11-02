import logging
import os
import nltk
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.stem.porter import PorterStemmer

from keywords_base import KeywordFinderBase


class KeywordFinderNLTK(KeywordFinderBase):
    """ Class for finding text keywords using the NLTK framework """
    min_bigram_freq = 2         # bi-gram finding threshold

    def __init__(self):
        # add this files directory to data search path
        nltk.data.path.extend([os.path.dirname(os.path.realpath(__file__))])
        pass

    def _get_available_languages(self):
        """ Get available languages by listing nltk's stopwords files """
        return stopwords.fileids()

    def detect_language(self, text):
        """ Detect language of text by using nltk's stopwords for comparison.

        Args:
            text: string to perform language detection on
        Returns:
            String containing the name of detected language.

        """
        language_ratios = {}
        words = set([word.lower() for word in nltk.word_tokenize(text) if len(word)>2])

        for language in self._get_available_languages():
            stopwords_set = set(stopwords.words(language))
            common_elements = words.intersection(stopwords_set)
            language_ratios[language] = len(common_elements)

        return max(language_ratios, key=language_ratios.get)

    def get_keywords(self, text, language=None):
        """ Get the list of keywords for passed text.

        Args:
            text: string to extract keywords from
            language: optional language string
        Return:
            List of keywords.

        """
        text = unicode(text)
        if language is not None:
            if language not in self._get_available_languages():
                logging.warn("User passed an unsupported language: %s. Falling back to: %s." % \
                                                                    (language, self.default_lang))
                language = self.default_lang
        else:
            language = self.detect_language(text)

        # load stopwords (words common in given language)
        stop_words = stopwords.words(language)
        stop_words = [word.decode("utf-8") for word in stop_words]  # fix to a bug in nltk

        # split text into words
        words = [word for word in nltk.wordpunct_tokenize(text) if len(word)>2 and\
                                                                word.lower() not in stop_words]

        # find bi-grams (two word collocations)
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(self.min_bigram_freq)
        bigrams = finder.nbest(bigram_measures.pmi, 5)

        # this whole part below could be shortened by a few loops, but readability would suffer
        # convert words to stems, saving original words for stems in a dictionary
        stemmer = PorterStemmer()
        original_words = {}
        stemmed_words = []
        for word in words:
            stem = stemmer.stem(word).lower()
            original_words[stem] = word  # TODO: handle most popular word for stem
            stemmed_words.append(stem)

        # find most frequent words, substitute stems by saved original words
        top_words = {original_words[word]:freq for word, freq in\
                                                            nltk.FreqDist(stemmed_words).items()}

        # exclude words already in bigrams
        expanded_bigrams = [word for bigram in bigrams for word in bigram]
        top_words = {word: freq for word, freq in top_words.items()\
                                                                if word not in expanded_bigrams}

        return self._filter_keywords(top_words, 0.4) + [" ".join(bigram) for bigram in bigrams]
