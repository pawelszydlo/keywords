from calais import Calais


class KeywordFinderCalais:
    """ Class for finding text keywords using the Calais API """
    API_KEY = "seffdjarup7phnn8z45f6mt6"

    def get_keywords(self, text):
        """ Get the list of keywords for passed text. """
        try:
            calais = Calais(self.API_KEY, submitter="python-calais demo")
            calais.processing_directives["enableMetadataType"] = "SocialTags"
            result = calais.analyze(text)
            return [tag["name"] for tag in result["socialTag"] if tag["importance"] > 1]
        except: # I know pokemon exception catching is bad, but it's some shady external lib
            return []