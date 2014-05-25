import pyramid

class Acl(object):
    public_paths = [
        'login',
        'public',
        'oauth'
    ]

    def __call__(self, event):
        session = event.request.session
        path = event.request.environ.get('PATH_INFO').split('/')

        if 'user' not in session and path[1] not in Acl.public_paths:
            raise pyramid.httpexceptions.HTTPFound(location='/login')
