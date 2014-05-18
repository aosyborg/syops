from syopsui.library.view import Abstract
from syopsui.models.team import Team
from syopsui.models.user import User
from syopsui.modules.default.forms.usereditform import UserEditForm
from syopsui.modules.default.forms.teameditform import TeamEditForm

class Admin(Abstract):

    def manage_teams(self):
        return self.render(
            'syopsui:modules/default/templates/admin/manage-teams.pt', {
            'page_title': 'Manage Teams',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'teams': Team.get_list(self.session['user'].id),
            'team_form': TeamEditForm(self.request)
            }, request=self.request)

    # TODO: make this a super user action
    def manage_users(self):
        return self.render(
            'syopsui:modules/default/templates/admin/manage-users.pt', {
            'page_title': 'Manage Users',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'users': User.get_list(),
            'user_form': UserEditForm(self.request)
            }, request=self.request)
