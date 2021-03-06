from functools import partial
import json
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import urlopen
    from urllib import urlencode


def utf8_encode(s):
    return s if isinstance(s, bytes) else s.encode('utf8')


def utf8_encode_dict_values(d):
    return {k: utf8_encode(v) for k, v in d.items()}


class EtherpadException(Exception): pass


class EtherpadLiteClient(object):

    def __init__(self, base_params={}, base_url='http://140.114.79.181:9001/api', #'https://clc-etherpad.herokuapp.com/api'
                       api_version='1.2.13', timeout=20):
        self.api_version = api_version
        self.base_params = utf8_encode_dict_values(base_params)
        self.base_url = base_url
        self.timeout = timeout

    def __call__(self, path, **params):
        params = utf8_encode_dict_values(params)
        data = urlencode(dict(self.base_params, **params)).encode('ascii')
        url = '%s/%s/%s' % (self.base_url, self.api_version, path)
        r = json.loads(urlopen(url, data, self.timeout).read().decode('utf-8'))
        if not r or not isinstance(r, dict):
            raise EtherpadException('API returned: %s' % r)
        if r.get('code') != 0:
            raise EtherpadException(r.get('message', r))
        return r.get('data')

    def __getattr__(self, name):
        return partial(self, name)
