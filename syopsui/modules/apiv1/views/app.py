from syopsui.library.view import Abstract
from syopsui.models.app import App as AppModel
from syopsui.models.release import Release as Release
from syopsui.modules.default.forms.appeditform import AppEditForm
from syopsui.modules.default.forms.releaseform import ReleaseForm

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

    def new_release(self):
        form = ReleaseForm(self.request)
        if not form.is_valid():
            return form.get_errors()

        release = Release(data=self.request.params)
        return release.create()
