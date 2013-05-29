from PySide.QtCore import QObject
from greentree.error import NoViewSelected


class Signal(object):

    def __init__(self, name, view_name, args=(), kwargs={}):
        self.name = name
        self.view_name = view_name
        self.args = (args, kwargs)


class ControllerData(object):

    def __init__(self):
        self.selected_view = None
        self.signals = []
        self.signals_end = []

    def add_view_signal(self, view_name, signal_name, *args, **kwargs):
        self.signals.append(
            Signal(signal_name, view_name, args, kwargs)
        )

    def add_view_signal_at_end(self, view_name, signal_name, *args, **kwargs):
        self.signals_end.append(
            Signal(signal_name, view_name, args, kwargs)
        )

    def add_binder_signal(self, signal_name, *args, **kwargs):
        self.add_view_signal(None, signal_name, *args, **kwargs)

    def add_binder_signal_at_end(self, signal_name, *args, **kwargs):
        self.add_view_signal_at_end(None, signal_name, *args, **kwargs)

    def select_view(self, name, hide_rest=False):
        self.selected_view = name
        if hide_rest:
            self.add_binder_signal_at_end('hide_all', name)

    def add_signal(self, signal_name, *args, **kwargs):
        if not self.selected_view:
            raise NoViewSelected()

        self.add_view_signal(self.selected_view, signal_name, *args, **kwargs)

    def get_signals(self):
        reversed_end = list(reversed(self.signals_end))
        return self.signals + reversed_end


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent=parent)

    def do_action(self, name, *args, **kwargs):
        method = getattr(self, name)
        self.args = args
        self.kwargs = kwargs

        self.data = ControllerData()
        self.before_action()
        method(*args, **kwargs)
        self.after_action()
        return self.data

    def before_action(self):
        pass

    def after_action(self):
        pass
