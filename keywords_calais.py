import urllib
import urllib2
import logging
try:
    import simplejson as json
except ImportError:
    import json


class KeywordFinderCalais:
    """ Class for finding text keywords using the Calais API """
    API_KEY = ""

    def __init__(self, api_key):
        """ Pass your Calais API key. """
        self.API_KEY = api_key

    def _get_calais_response(self, text, key):
        """ Get json response from Calais web API. """
        params_template = """
        <c:params xmlns:c="http://s.opencalais.com/1/pred/"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <c:processingDirectives %s> </c:processingDirectives>
            <c:userDirectives c:allowDistribution="false" c:allowSearch="false" c:submitter="wgt">
            </c:userDirectives>
        </c:params>
        """
        processing_directives = {"contentType":"TEXT/RAW",
                                 "outputFormat":"application/json",
                                 "calculateRelevanceScore":"true",
                                 "enableMetadataType":"SocialTags",
                                 "omitOutputtingOriginalText":"true"}

        config = params_template % \
                 (" ".join('c:%s="%s"' % (k,v) for (k,v) in processing_directives.items()))

        params = urllib.urlencode({'licenseID':key, 'content':text, 'paramsXML':config})
        headers = {"Content-type":"application/x-www-form-urlencoded",
                     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/536.5\
                                    (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"}

        raw_data = ""
        try:
            request = urllib2.Request("http://api.opencalais.com/enlighten/rest/", params, headers)
            response = urllib2.urlopen(request, timeout=1)
            raw_data = response.read()
        except urllib2.URLError:
            logging.error("Calais server did not respond in time.")

        return raw_data

    def _simplify_response(self, json_response):
        """ Simplify the response from Calais server.
        This code comes from Jordan Dimov's python-calais module.

        """
        result = {}
        # First, resolve references
        for element in json_response.values():
            for k, v in element.items():
                if isinstance(v, unicode) and v.startswith("http://") and json_response.has_key(v):
                    element[k] = json_response[v]
        for k, v in json_response.items():
            if v.has_key("_typeGroup"):
                group = v["_typeGroup"]
                if not result.has_key(group):
                    result[group] = []
                del v["_typeGroup"]
                v["__reference"] = k
                result[group].append(v)
        return result

    def get_keywords(self, text):
        """ Get the list of keywords for passed text. """
        raw_data = self._get_calais_response(text, self.API_KEY)
        data = None
        try:
            data = json.loads(raw_data)
            data = self._simplify_response(data)
            data = data.get("socialTag", None)
        except ValueError:
            logging.error("JSON could not parse the Calais response.")

        if data:
            return [tag["name"] for tag in data if tag["importance"] > 1]
        else:
            return []
