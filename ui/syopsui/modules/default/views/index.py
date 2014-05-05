from syopsui.library.view import Abstract

class Index(Abstract):

    def index(self):
        if 'user' not in self.session:
            return self.redirect('/login')

        return self.render('syopsui:modulels/default/templates/index/index.pt', {
                }, request=self.request)
