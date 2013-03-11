from PySide.QtCore import Qt
from PySide.QtGui import QWidget
from .error import MissingMethodImplementationError


class ViewType(type(Qt), type):

    main_class = 'greentree.view.View'

    def __init__(cls, name, bases, dct):
        def check_if_methods_are_implemented(methods_name):
            for name in methods_name:
                if not hasattr(cls, name):
                    raise MissingMethodImplementationError(cls, name)
        #-----------------------------------------------------------------------
        super(ViewType, cls).__init__(name, bases, dct)
        classfullname = '%s.%s' % (cls.__module__, cls.__name__)
        if classfullname != ViewType.main_class:
            check_if_methods_are_implemented(['create_design'])


class View(QWidget):

    __metaclass__ = ViewType

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.create_design()
        self.connect_signals()

    def connect_signals(self):
        pass