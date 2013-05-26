from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout
from greentree.signals import SignalReadyMixin

from .error import MissingMethodImplementationError


class BinderType(type(Qt), type):

    main_class = 'greentree.binder.Binder'

    def __init__(cls, name, bases, dct):
        def check_if_methods_are_implemented(methods_name):
            for name in methods_name:
                if not hasattr(cls, name):
                    raise MissingMethodImplementationError(cls, name)
        #----------------------------------------------------------------------
        super(BinderType, cls).__init__(name, bases, dct)
        classfullname = '%s.%s' % (cls.__module__, cls.__name__)
        if classfullname != BinderType.main_class:
            check_if_methods_are_implemented(['create_controller'])


class Binder(QWidget, SignalReadyMixin):

    __metaclass__ = BinderType

    def __init__(self, parent=None):
        super(Binder, self).__init__(parent=parent)
        self.signals_init()
        self._parent = parent
        self.views = {}

        self.generate_views()
        self.controller = self.create_controller()

        layout = self.create_layout()
        self.add_all_views_to_layout(layout)

    def add_view(self, view_cls):
        view = view_cls(binder=self, parent=self._parent)
        self.views[view.name()] = view

    def add_all_views_to_layout(self, layout):
        for name, view in self.views.items():
            layout.addWidget(view)

    def make_controller_action(self, method_name, *args, **kwargs):
        def emit_binder_signals(controller_data):
            for signal_name, (args, kwargs) in controller_data.binder_signals.items():
                self.gtemit(signal_name, *args, **kwargs)

        def emit_views_signals(controller_data):
            for view_name, data in controller_data.view_signals.items():
                view = self.views[view_name]
                for signal_name, (args, kwargs) in data.items():
                    view.gtemit(signal_name, *args, **kwargs)

        controller_data = self.controller.do_action(
            method_name, *args, **kwargs)

        emit_binder_signals(controller_data)
        emit_views_signals(controller_data)

    def hide_all(self, except_name=None):
        for view_name, view in self.views.items():
            if view_name == except_name:
                view.show()
            else:
                view.hide()

    def create_layout(self):
        return QVBoxLayout(self)

    def generate_views(self):
        pass

    def generate_signals(self):
        super(Binder, self).generate_signals()
        self.add_signal(self.hide_all, 'hide_all')
