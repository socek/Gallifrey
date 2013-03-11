from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout
from .error import MissingMethodImplementationError


class BinderType(type(Qt), type):

    main_class = 'greentree.binder.Binder'

    def __init__(cls, name, bases, dct):
        def check_if_methods_are_implemented(methods_name):
            for name in methods_name:
                if not hasattr(cls, name):
                    raise MissingMethodImplementationError(cls, name)
        #-----------------------------------------------------------------------
        super(BinderType, cls).__init__(name, bases, dct)
        classfullname = '%s.%s' % (cls.__module__, cls.__name__)
        if classfullname != BinderType.main_class:
            check_if_methods_are_implemented(['create_controller'])


class Binder(QWidget):

    __metaclass__ = BinderType

    def __init__(self, parent=None):
        super(Binder, self).__init__(parent=parent)
        self._parent = parent
        self.views = {}
        self.generate_views()
        self.connect_signals()
        self.controller = self.create_controller()

        layout = self.create_layout()
        self.add_all_views_to_layout(layout)

    def add_view(self, name, view_cls):
        self.views[name] = view_cls(parent=self._parent)

    def add_all_views_to_layout(self, layout):
        for name, view in self.views.items():
            layout.addWidget(view)

    def make_controller_action(self, method_name, *args, **kwargs):
        method = getattr(self.controller, method_name)
        controller_data = method(*args, **kwargs)

        for signal_name, args in controller_data.binder_signals.items():
            signal = getattr(self, signal_name)
            signal.emit(*args)

        for view_name, data in controller_data.view_signals.items():
            view = self.views[view_name]
            for signal_name, args in data.items():
                signal = getattr(view, signal_name)
                signal.emit(*args)

    def create_layout(self):
        return QVBoxLayout(self)

    def connect_signals(self):
        pass

    def generate_views(self):
        pass
