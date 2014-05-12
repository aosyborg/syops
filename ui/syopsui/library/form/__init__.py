class Abstract(object):
    def __init__(self, request=None):
        self.request = request
        self.elements = {}
        self.init()

        # Populate form with request
        for name, element in self.elements.items():
            if name in request.params:
                element.set(request.params[name])

    def init(self):
        pass

    def is_valid(self):
        for name, element in self.elements.items():
            if not element.is_valid(self.request):
                return False
        return True

    def add_element(self, element):
        self.elements[element.name] = element
        return self

    def get_element(self, name):
        if name not in self.elements:
            raise Exception('Element "%s" not found' % name)

        return self.elements[name]

    def get_data(self):
        data = {}
        for name, element in self.elements.items():
            data[name] = element.value
        return data
