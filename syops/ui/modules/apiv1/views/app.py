from syops.lib.view import Abstract
from syops.lib.models.app import App as AppModel
from syops.lib.models.team import Team
from syops.lib.models.release import Release as Release
from syops.lib.models.github import Github
from syops.ui.modules.default.forms.appeditform import AppEditForm
from syops.ui.modules.default.forms.releaseform import ReleaseForm

class App(Abstract):

    def edit(self):
        form = AppEditForm(self.request)
        if not form.is_valid():
            return form.get_errors()

        app = AppModel(data=self.request.params)
        app.save()
        return app.to_json()

    def delete(self):
        app_id = self.request.params.get('app_id')
        app = AppModel(app_id)
        return app.delete()

    def list_branches(self):
        user = self.session['user']
        app_id = self.request.params.get('app_id')
        app = AppModel(app_id)
        team = Team(app.team_id)

        resource = '/repos/%s/%s/branches' % (app.github_owner, app.github_repo)
        return Github.get(resource, access_token=user.access_token)

    def new_release(self):
        form = ReleaseForm(self.request)
        if not form.is_valid():
            return form.get_errors()

        release = Release(data=self.request.params)
        return release.save()

    def release(self):
        release_id = self.request.params.get('release_id')
        release = Release(release_id)
        release.release_status_id += 1
        return release.save()
