from syopsui.library.view import Abstract
from syopsui.modules.default.forms.login import LoginForm

class User(Abstract):

    def login(self):
        values = {}
        form = LoginForm(self.request)

        if self.request.POST:
            user = form.is_valid()
            if not user:
                values['error'] = 'Username or password is incorrect'
            else:
                self.session['user'] = user
                return self.redirect('/')

        values['page_title'] = 'Login'
        values['form'] = form
        return self.render(
            'syopsui:modules/default/templates/user/login.pt',
            values, request=self.request)
