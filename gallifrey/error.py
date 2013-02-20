class MissingMethodImplementationError(Exception):
    def __init__(self, cls, method_name):
        self.cls = cls
        self.method_name = method_name

    def __str__(self):
        return ' '.join([str(self.cls), self.method_name])
