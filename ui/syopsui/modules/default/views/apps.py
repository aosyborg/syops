from syopsui.library.view import Abstract

class Apps(Abstract):

    def index(self):
        values = {}

        values['page_title'] = 'Applications'
        return self.render(
            'syopsui:modules/default/templates/apps/index.pt',
            values, request=self.request)
