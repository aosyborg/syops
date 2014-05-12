from syopsui.library.view import Abstract
from syopsui.models.team import Team

class Index(Abstract):

    def index(self):
        return self.render(
            'syopsui:modules/default/templates/index/index.pt', {
            'page_title': 'Welecome',
            'team_apps': Team.get_team_apps(self.session['user'].id),
            }, request=self.request)
