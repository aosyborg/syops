from syops.lib.form import Abstract as FormAbstract
from syops.lib.form.elements.input import Input
from syops.ui.models.user import User

class LoginForm(FormAbstract):
    def init(self):
        # Email
        email = Input(name='email', type='email')
        email.add_attribute('class', 'form-control')
        email.add_attribute('id', 'email-input')
        self.add_element(email)

        # Password
        password = Input(name='password', type='password')
        password.add_attribute('class', 'form-control')
        password.add_attribute('id', 'email-input')
        self.add_element(password)

        # Remember me
        remember = Input(name="remember", type='checkbox')
        remember.add_attribute('checked', 'checked')
        remember.add_attribute('id', 'remember-input')
        self.add_element(remember)

    def is_valid(self):
        email = self.elements['email'].value
        password = self.elements['password'].value
        return User.login(email, password)
