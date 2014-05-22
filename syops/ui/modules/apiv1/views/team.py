from syops.lib.view import Abstract
from syops.lib.models.github import Github

class Team(Abstract):

    def list_orgs(self):
        user = self.session['user']
        return Github.get('/user/orgs', access_token=user.access_token)

    def list_repos(self):
        user = self.session['user']
        return Github.get('/user/repos', access_token=user.access_token)
