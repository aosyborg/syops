from syopsui.library.view import Abstract

class Error(Abstract):

    def not_found(self):
        self.request.response.status = 404
        return self.render(
            'syopsui:modules/default/templates/error/404.pt', {
                'page_title': 'Error 404'
            }, request=self.request)
