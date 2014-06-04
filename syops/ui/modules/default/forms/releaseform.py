from syops.lib.form import Abstract as FormAbstract
from syops.lib.form.elements.input import Input
from syops.lib.form.elements.select import Select
from syops.lib.form.elements.textarea import Textarea

class ReleaseForm(FormAbstract):
    def init(self):
        # Version
        version = Input(name='version', type='input')
        version.add_attribute('class', 'form-control')
        version.add_attribute('id', 'release-version')
        version.add_attribute('placeholder', '0.1-1')
        self.add_element(version)

        # Branch (javascript will populate this)
        branch = Select(name='tagged_branch')
        branch.add_attribute('class', 'form-control')
        branch.add_attribute('id', 'tagged-branch')
        self.add_element(branch)

        # Description
        description = Textarea(name='description')
        description.add_attribute('class', 'form-control')
        description.add_attribute('id', 'release-description')
        self.add_element(description)
