#!/usr/bin/env python
""" Simple tool for testing the keyword finders from command line. """
import sys
import codecs

from keywords_calais import KeywordFinderCalais
from keywords_nltk import KeywordFinderNLTK
from keywords_python import KeywordFinderPython

if __name__ == "__main__":
    VALID_METHODS = ("calais", "nltk", "pure")

    if len(sys.argv)<2:
        print "Usage: %s method [text_file]\nmethod is one of (%s)" % \
              (__file__, ", ".join(VALID_METHODS))
        sys.exit(1)
    else:
        method = sys.argv[1]
        if method not in VALID_METHODS:
            print "Invalid method: %s" % (sys.argv[1])
            sys.exit(2)

    if len(sys.argv)>2:
        try:
            text = codecs.open(sys.argv[2], encoding='utf-8', mode="r").read()
        except IOError:
            print "Can't read %s." % (sys.argv[2])
            sys.exit(2)
    else:
        text = raw_input("Paste your text now:\n\n")

    if method == "calais":
        keyword_finder = KeywordFinderCalais("xxx")
    elif method == "nltk":
        keyword_finder = KeywordFinderNLTK()
    else:
        keyword_finder = KeywordFinderPython()

    keywords = keyword_finder.get_keywords(unicode(text))
    print u", ".join(keywords)
