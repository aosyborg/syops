from syopsui.library.view import Abstract
from pyramid.response import Response

class User(Abstract):

    def login(self):
        return self.render(
            'syopsui:modules/default/templates/user/login.pt', {
                'hello': 'world'
            }, request=self.request)
