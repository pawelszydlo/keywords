class KeywordFinderBase:
    """ Base class for finding text keywords. Not really needed in this project.

    Methods you must overwrite:
        get_keywords

    """
    default_lang = "english"    # fallback language if user supplies wrong one

    def _filter_keywords(self, word_freq_dict, tag_threshold=0.20):
        """ Select top keywords based on calculated frequency threshold. This implementation
        is obviously flawed. More research and more advanced math is needed here.

        Args:
            word_freq_dict: dictionary with items in the form word->frequency
            tag_threshold: optional threshold (multiplier of max frequency) for keywords to include
        Returns:
            List containing top words.

        """
        if len(word_freq_dict)==0:
            return []
        top_words = sorted(word_freq_dict.items(), key=lambda x: x[1], reverse=True)
        max_freq = top_words[0][1] if len(top_words)>0 else 0
        avg_freq = sum(word_freq_dict.values())/len(word_freq_dict)

        if max_freq == avg_freq:   # hack, need to return something...
            return [word[0] for word in top_words[:3]]

        # don't let the threshold fall below avarage
        threshold = max(avg_freq, max_freq*tag_threshold)

        return [word[0] for word in top_words if word[1] > threshold]

    def get_keywords(self, text, language=None):
        raise NotImplementedError("This needs to be implemented")


class KeywordFinderException(Exception):
    """ Base class for exceptions in this module. """
    pass
