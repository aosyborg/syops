from syopsui.library.view import Abstract
from syopsui.models.app import App
from syopsui.models.team import Team
from syopsui.modules.default.forms.appeditform import AppEditForm

class Teams(Abstract):

    def overview(self):
        team_id = self.request.params.get('id')

        return self.render(
            'syopsui:modules/default/templates/teams/overview.pt', {
            'page_title': 'Team Overview',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'app_form': AppEditForm(self.request),
            'apps': App.get_list(team_id),
            'team': Team(team_id)
            }, request=self.request)
