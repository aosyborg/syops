import json
from httplib2 import Http
from urllib import urlencode

from syops.lib.application import Application

class Github(object):
    PROTOCAL = 'https'
    BASE_URL = 'api.github.com'

    @staticmethod
    def post(path, params={}, access_token=None):
        if access_token:
            params['access_token'] = access_token

        url = '%s://%s%s' % (Github.PROTOCAL, Github.BASE_URL, path)
        headers, content = Http().request(url, 'POST', urlencode(params))
        return json.loads(content)

    @staticmethod
    def get(path, params={}, access_token=None):
        if access_token:
            params['access_token'] = access_token

        url = '%s://%s%s?%s' % (Github.PROTOCAL, Github.BASE_URL, path,urlencode(params))
        headers, content = Http().request(url, 'GET')
        return json.loads(content)

    @staticmethod
    def get_access_token(code):
        url = 'https://github.com/login/oauth/access_token'
        headers = {'Accept': 'application/json'}
        params = {
            'client_id': Application.OAUTH_GITHUB_CLIENT_ID,
            'client_secret': Application.OAUTH_GITHUB_CLIENT_SECRET,
            'code': code
        }

        # Request access token
        headers, content = Http().request(url, 'POST', headers=headers, body=urlencode(params))
        content = json.loads(content)
        return content.get('access_token');
