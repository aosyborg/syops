from syops.lib.form import Abstract as FormAbstract
from syops.lib.form.elements.input import Input
from syops.lib.models.user import User

class UserEditForm(FormAbstract):
    def init(self):
        # Name
        email = Input(name='name', type='input')
        email.add_attribute('class', 'form-control')
        email.add_attribute('id', 'user-name')
        self.add_element(email)

        # Email
        email = Input(name='email', type='email')
        email.add_attribute('class', 'form-control')
        email.add_attribute('id', 'user-email')
        self.add_element(email)

        # Password
        password = Input(name='password', type='password')
        password.add_attribute('class', 'form-control')
        password.add_attribute('id', 'user-email')
        self.add_element(password)

        # Is admin
        remember = Input(name="is-admin", type='checkbox')
        remember.add_attribute('id', 'user-is-admin')
        self.add_element(remember)

    def is_valid(self):
        # TODO: add validation
        return True
