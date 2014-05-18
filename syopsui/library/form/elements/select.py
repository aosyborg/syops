from syopsui.library.form.elements import Abstract

class Select(Abstract):
    def __init__(self, name):
        super(Select,self).__init__()
        self.name = name
        self.options = []

    def add_option(self, option):
        self.options.append(option)
        return self

    def __str__(self):
        attributes = ' '.join(['%s="%s"' % (name, value) for name, value in
                self.attributes.items()])
        options = ''.join([option.__str__() for option in self.options])

        return '<select name="%s" %s >%s</select>' % (self.name, attributes, options)
