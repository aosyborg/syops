from syops.lib.form import Abstract as FormAbstract
from syops.lib.form.elements.input import Input
from syops.lib.form.validators.teamownerid import TeamOwnerId
from syops.lib.models.team import Team

class TeamEditForm(FormAbstract):
    def init(self):
        # Name
        email = Input(name='name', type='input')
        email.add_attribute('class', 'form-control')
        email.add_attribute('id', 'team-name')
        self.add_element(email)

        # Is organization
        org = Input(name='is_organization', type='input')
        self.add_element(org)

        # Owner
        owner = Input(name='owner_id', type="hidden")
        owner.add_validator(TeamOwnerId())
        self.add_element(owner)
