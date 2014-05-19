from syops.lib.view import Abstract
from syops.lib.models.app import App
from syops.lib.models.team import Team
from syops.lib.models.debs import Debs
from syops.ui.modules.default.forms.releaseform import ReleaseForm
from syops.ui.modules.default.forms.appeditform import AppEditForm

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

    def edit(self):
        app_id = self.request.params.get('id')
        app = App(app_id)

        return self.render(
            'syops.ui:modules/default/templates/apps/edit.pt', {
            'page_title': 'Application Edit',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            'app_form': AppEditForm(data=app.to_json()),
            'app': app
            }, request=self.request)
