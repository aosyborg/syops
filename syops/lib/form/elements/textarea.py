from syops.lib.form.elements import Abstract

class Textarea(Abstract):
    def __init__(self, name):
        super(Textarea,self).__init__()
        self.name = name

    def __str__(self):
        attributes = ' '.join(['%s="%s"' % (name, value) for name, value in
                self.attributes.items()])

        return '<textarea name="%s" %s></textarea>' % (self.name, attributes)
