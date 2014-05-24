from syops.lib.form import Abstract as FormAbstract
from syops.lib.form.elements.input import Input
from syops.lib.form.elements.textarea import Textarea
from syops.lib.form.validators.teamownerid import TeamOwnerId
from syops.lib.models.team import Team

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
        owner = Input(name='github_owner', type='input')
        owner.add_attribute('class', 'form-control')
        owner.add_attribute('id', 'app-owner')
        self.add_element(owner)

        # Github repo
        repo = Input(name='github_repo', type='input')
        repo.add_attribute('class', 'form-control')
        repo.add_attribute('id', 'app-repo')
        self.add_element(repo)

        # Docs URL
        docs = Input(name='doc_url', type='input')
        docs.add_attribute('class', 'form-control')
        docs.add_attribute('id', 'app-docs')
        self.add_element(docs)

        # Build instructions
        build = Textarea(name='build_instructions')
        build.add_attribute('class', 'form-control')
        build.add_attribute('id', 'app-build_instructions')
        build.add_attribute('rows', '20')
        self.add_element(build)
