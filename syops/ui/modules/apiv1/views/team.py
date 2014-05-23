from syops.lib.view import Abstract
from syops.lib.models.team import Team as TeamModel
from syops.lib.models.github import Github

class Team(Abstract):

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
