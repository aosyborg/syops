from syops.lib.view import Abstract
from syops.lib.models.github import Github

class Team(Abstract):

    def list_repos(self):
        user = self.session['user']
        return Github.get('/user/repos', access_token=user.access_token)
