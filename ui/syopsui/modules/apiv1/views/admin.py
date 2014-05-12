from syopsui.library.view import Abstract
from syopsui.models.team import Team
from syopsui.models.user import User
from syopsui.modules.default.forms.usereditform import UserEditForm
from syopsui.modules.default.forms.teameditform import TeamEditForm

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

    def edit_team(self):
        form = TeamEditForm(self.request)
        if not form.is_valid():
            return form.get_errors()

        team = Team(data=form.get_data())
        team.save()
        return team.to_json()

    def delete_team(self):
        team_id = self.request.params.get('team_id')
        team = Team(team_id)
        return team.delete()

