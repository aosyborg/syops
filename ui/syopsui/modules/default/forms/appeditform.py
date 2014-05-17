from syopsui.library.form import Abstract as FormAbstract
from syopsui.library.form.elements.input import Input
from syopsui.library.form.validators.teamownerid import TeamOwnerId
from syopsui.models.team import Team

class AppEditForm(FormAbstract):
    def init(self):
        # Name
        email = Input(name='name', type='input')
        email.add_attribute('class', 'form-control')
        email.add_attribute('id', 'app-name')
        self.add_element(email)

        # Github clone URL
        url = Input(name='clone_url', type='input')
        url.add_attribute('class', 'form-control')
        url.add_attribute('id', 'app-clone-url')
        self.add_element(url)

        # Github owner
        url = Input(name='github_owner', type='input')
        url.add_attribute('class', 'form-control')
        url.add_attribute('id', 'app-owner')
        self.add_element(url)

        # Github repo
        url = Input(name='github_repo', type='input')
        url.add_attribute('class', 'form-control')
        url.add_attribute('id', 'app-repo')
        self.add_element(url)
