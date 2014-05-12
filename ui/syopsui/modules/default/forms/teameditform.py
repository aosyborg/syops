from syopsui.library.form import Abstract as FormAbstract
from syopsui.library.form.elements.input import Input
from syopsui.library.form.validators.teamownerid import TeamOwnerId
from syopsui.models.team import Team

class TeamEditForm(FormAbstract):
    def init(self):
        # Name
        email = Input(name='name', type='input')
        email.add_attribute('class', 'form-control')
        email.add_attribute('id', 'team-name')
        self.add_element(email)

        # Owner
        owner = Input(name='owner_id', type="hidden")
        owner.add_validator(TeamOwnerId())
        self.add_element(owner)
