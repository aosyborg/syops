from urllib import urlencode

from syops.lib.view import Abstract
from syops.lib.models.user import User

class Invite(Abstract):

    def request_invite(self):
        error = None

        # Handle form submission
        if self.request.POST:
            email = self.request.params.get('email')
            user = User.build_from_email(email)
            if user:
                error = True
            else:
                user = User()
                user.name = 'Unknown'
                user.email = email
                user.access_token = 'None'
                user.avatar_url = 'None'
                user.save()
                return self.redirect('/invite/thanks')

        return self.render(
            'syops.ui:modules/default/templates/invite/request.pt', {
            'page_title': 'Request invite',
            'error': error
            }, request=self.request)

    def thanks(self):
        return self.render(
            'syops.ui:modules/default/templates/invite/thanks.pt', {
            'page_title': 'Request invite'
            }, request=self.request)
