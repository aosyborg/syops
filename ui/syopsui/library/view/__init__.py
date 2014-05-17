from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

class Abstract(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.init()

    def init(self):
        # TODO: Fix this
        if not 'user' in self.session and self.request.view_name != 'login':
            return self.redirect('/login')

    def render(self, renderer_name, value, request=None, package=None):
        # Defaults
        page_variables = {
            'page_title': 'SyOps'
        }
        value = dict(page_variables.items() + value.items())

        # Set request
        if request is None:
            request = self.request

        return render_to_response(renderer_name, value, request, package)

    def redirect(self, location):
        return HTTPFound(location=location)
