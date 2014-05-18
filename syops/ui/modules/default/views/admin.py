from syops.lib.view import Abstract
from syops.ui.models.team import Team
from syops.ui.models.user import User
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
        return self.render(
            'syops.ui:modules/default/templates/admin/manage-users.pt', {
            'page_title': 'Manage Users',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'users': User.get_list(),
            'user_form': UserEditForm(self.request)
            }, request=self.request)
