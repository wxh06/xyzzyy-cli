from json import loads
import re
from urllib.parse import urlencode
from urllib.request import urlopen, Request


class Session:

    def __init__(self, site, pj):
        self.site = site
        self.pj = pj

        class Data:
            def __init__(self, session):
                self.session = session

            def __getattr__(self, name):
                match = re.fullmatch(r'([a-z]+)_([A-Za-z]+)', name)
                if match:
                    module, sAct = match.groups()

                    def _act(**kwargs):
                        return self.session.act(module, sAct, **kwargs)
                    return _act
                raise AttributeError
        self.data = Data(self)

    def act(self, module, sAct, **kwargs):
        data = loads(urlopen(Request(
            f'{self.site}/data/module/{module}/all.asp?sAct={sAct}',
            urlencode(kwargs).encode(),
            headers={'Cookie': f'pj={self.pj}'}
        )).read())
        try:
            assert data['sRet'] == 'succeeded', data
            return data
        except AssertionError:
            return None
