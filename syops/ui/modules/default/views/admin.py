from urllib import urlencode

from syops.lib.view import Abstract
from syops.lib.application import Application
from syops.lib.models.team import Team
from syops.lib.models.user import User
from syops.lib.models.github import Github
from syops.ui.modules.default.forms.usereditform import UserEditForm
from syops.ui.modules.default.forms.teameditform import TeamEditForm

class Admin(Abstract):

    def manage_teams(self):
        return self.render(
            'syops.ui:modules/default/templates/admin/manage-teams.pt', {
            'page_title': 'Manage Teams',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'teams': Team.get_list(self.session['user'].id),
            'team_form': TeamEditForm(self.request)
            }, request=self.request)

    # TODO: make this a super user action
    def manage_users(self):
        # Build new user oauth url
        params = {
            'client_id': Application.OAUTH_GITHUB_CLIENT_ID,
            'scope': 'user:email,repo'
        }
        new_user_url = '%s?%s' % (Application.OAUTH_GITHUB_URL, urlencode(params))
        print new_user_url

        return self.render(
            'syops.ui:modules/default/templates/admin/manage-users.pt', {
            'page_title': 'Manage Users',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'users': User.get_list(),
            'new_user_url': new_user_url,
            'user_form': UserEditForm(self.request)
            }, request=self.request)

    # Note: called after user authenticates via oauth
    def add_user(self):
        #oauth_code = self.request.params.get('code')
        #access_token = Github.get_access_token(oauth_code)

        User.create_from_access_token('a48cf86df99de8d543dfa84b0fcc40dadd265f20')
