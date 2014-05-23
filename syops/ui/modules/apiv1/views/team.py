from syops.lib.view import Abstract
from syops.lib.models.team import Team as TeamModel
from syops.lib.models.github import Github
from syops.ui.modules.default.forms.teameditform import TeamEditForm

class Team(Abstract):

    def edit(self):
        form = TeamEditForm(self.request)
        if not form.is_valid():
            return form.get_errors()

        team = TeamModel(data=form.get_data())
        team.save()
        return team.to_json()

    def delete(self):
        team_id = self.request.params.get('team_id')
        team = Team(team_id)
        return team.delete()

    def list_orgs(self):
        user = self.session['user']
        return Github.get('/user/orgs', access_token=user.access_token)

    def list_repos(self):
        user = self.session['user']
        team_id = self.request.params.get('team_id')
        team = TeamModel(team_id)

        # If the team is an organization list org repos
        if team.is_organization:
            return Github.get('/orgs/%s/repos' % team.name, access_token=user.access_token)

        # Default to user repos
        return Github.get('/user/repos', access_token=user.access_token)
