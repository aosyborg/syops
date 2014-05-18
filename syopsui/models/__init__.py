class Abstract(object):
    data_manager = None

    def get_db_cursor(self):
        return self.data_manager.get_db_cursor()

    def get_model(self, Model):
        """
        Simply makes testing models eaiser
        """
        return Model()

    def cleanup(self):
        self.data_manager.cleanup()

    def to_json(self):
        json = {}
        for name, value in self.__dict__.items():
            if isinstance(value, (int, bool)):
                json[name] = value
            else:
                json[name] = str(value)

        return json
