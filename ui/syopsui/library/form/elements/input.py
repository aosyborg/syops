from syopsui.library.form.elements.abstract import Abstract

class Input(Abstract):
    def __init__(self, name, type='text'):
        super(Input,self).__init__()
        self.name = name
        self.type = type
        self.value = ''

    def __str__(self):
        attributes = ' '.join(['%s="%s"' % (name, value) for name, value in
                self.attributes.items()])
        return '<input type="%s" \
                       name="%s" \
                       value="%s" \
                       %s />' % (self.type, self.name, self.value, attributes)
