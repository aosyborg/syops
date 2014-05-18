from syops.lib.view import Abstract
from syops.lib.models.app import App
from syops.lib.models.team import Team
from syops.lib.models.debs import Debs
from syops.ui.modules.default.forms.releaseform import ReleaseForm

class Apps(Abstract):

    def overview(self):
        app_id = self.request.params.get('id')

        return self.render(
            'syops.ui:modules/default/templates/apps/overview.pt', {
            'page_title': 'Application Overview',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'app': App(app_id),
            'prod': Debs.get_latest_pkg(env='prod'),
            'qa': Debs.get_latest_pkg(env='qa'),
            'release_form': ReleaseForm(self.request)
            }, request=self.request)
