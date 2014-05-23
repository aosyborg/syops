from syops.lib.view import Abstract
from syops.lib.models.team import Team
from syops.lib.models.user import User
from syops.ui.modules.default.forms.usereditform import UserEditForm

class Admin(Abstract):

    def edit_user(self):
        form = UserEditForm(self.request)
        if not form.is_valid():
            return form.get_errors()

        user = User(data=self.request.params)
        user.save()
        return user.to_json()

    def delete_user(self):
        user_id = self.request.params.get('user_id')
        user = User(user_id)
        return user.delete()


