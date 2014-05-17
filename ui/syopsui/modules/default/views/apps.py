from syopsui.library.view import Abstract
from syopsui.models.app import App
from syopsui.models.team import Team
from syopsui.modules.default.forms.releaseform import ReleaseForm

class Apps(Abstract):

    def overview(self):
        app_id = self.request.params.get('id')

        return self.render(
            'syopsui:modules/default/templates/apps/overview.pt', {
            'page_title': 'Application Overview',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'app': App(app_id),
            'release_form': ReleaseForm(self.request)
            }, request=self.request)
