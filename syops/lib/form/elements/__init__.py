class Abstract(object):

    def __init__(self):
        self.attributes = {}
        self.validators = []

    def set(self, value):
        self.value = value

    def add_attribute(self, name, value):
        self.attributes[name] = value
        return self

    def add_validator(self, validator):
        self.validators.append(validator)
        return self

    def is_valid(self, request):
        for validator in self.validators:
            if not validator.is_valid(self, request):
                return False
        return True

    def __str__(self):
        return ''
