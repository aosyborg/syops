from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

class Abstract(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session

    def __call__(self):
        pass
        #if not 'user' in self.session and self.request.view_name != 'login':
        #    def redirect():
        #        return self.redirect('/login')
        #    return redirect

    def render(self, renderer_name, value, request=None, package=None):
        # Defaults
        page_variables = {
            'page_title': 'SyOps',
            'user_id': self.session['user'].id if 'user' in self.session else 0,
            'user': self.session['user'] if 'user' in self.session else None
        }
        value = dict(page_variables.items() + value.items())

        # Set request
        if request is None:
            request = self.request

        return render_to_response(renderer_name, value, request, package)

    def redirect(self, location):
        return HTTPFound(location=location)
