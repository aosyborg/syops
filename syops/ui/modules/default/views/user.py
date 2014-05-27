from urllib import urlencode

from syops.lib.view import Abstract
from syops.lib.application import Application
from syops.lib.models.user import User as UserModel
from syops.lib.models.github import Github

class User(Abstract):

    def login(self):
        # Build new user oauth url
        params = urlencode({
            'client_id': Application.OAUTH_GITHUB_CLIENT_ID,
            'scope': 'user:email,repo'
        })

        return self.render(
            'syops.ui:modules/default/templates/user/login.pt', {
            'github_login': '%s?%s' % (Application.OAUTH_GITHUB_URL, params),
            'page_title': 'Login'
            }, request=self.request)

    def logout(self):
        self.session.pop('user', None)
        return self.redirect('/login')

    # Note: called after user authenticates via oauth
    def oauth_callback(self):
        oauth_code = self.request.params.get('code')
        access_token = Github.get_access_token(oauth_code)
        user = UserModel.build_from_access_token(access_token)

        # Login failed
        if not user:
            return self.redirect('/invite/request')

        # Login successful
        self.session['user'] = user
        return self.redirect('/')
