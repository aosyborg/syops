from urllib import urlencode

from syops.lib.view import Abstract
from syops.lib.application import Application
from syops.lib.models.user import User as UserModel
from syops.lib.models.github import Github
from syops.ui.modules.default.forms.login import LoginForm

class User(Abstract):

    def login(self):
        values = {}
        form = LoginForm(self.request)

        # Attempt login on form submission
        if self.request.POST:
            user = form.is_valid()
            if not user:
                values['error'] = 'Username or password is incorrect'
            else:
                self.session['user'] = user
                return self.redirect('/')

        # Build new user oauth url
        params = urlencode({
            'client_id': Application.OAUTH_GITHUB_CLIENT_ID,
            'scope': 'user:email,repo'
        })

        values['github_login'] = '%s?%s' % (Application.OAUTH_GITHUB_URL, params)
        values['page_title'] = 'Login'
        values['form'] = form
        return self.render(
            'syops.ui:modules/default/templates/user/login.pt',
            values, request=self.request)

    # Note: called after user authenticates via oauth
    def oauth_callback(self):
        oauth_code = self.request.params.get('code')
        access_token = Github.get_access_token(oauth_code)

        user = UserModel.build_from_access_token(access_token)
        self.session['user'] = user
        return self.redirect('/')
