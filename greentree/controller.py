from PySide.QtCore import QObject
from greentree.error import NoViewSelected


class ControllerData(object):

    def __init__(self):
        self.binder_signals = {}
        self.view_signals = {}
        self.selected_view = None

    def view_select(self, name, hide_rest=False):
        self.selected_view = name
        if hide_rest:
            self.add_binder_signal('hide_all', name)

    def signal_view(self, signal_name, *args, **kwargs):
        if not self.selected_view:
            raise NoViewSelected()

        if not self.selected_view in self.view_signals:
            self.view_signals[self.selected_view] = {}

        self.view_signals[self.selected_view][signal_name] = (args, kwargs)

    def add_binder_signal(self, signal_name, *args, **kwargs):
        self.binder_signals[signal_name] = (args, kwargs)

    def add_view_signal(self, view_name, signal_name, *args, **kwargs):
        if not view_name in self.view_signals:
            self.view_signals[view_name] = {}
        self.view_signals[view_name][signal_name] = (args, kwargs)


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent=parent)

    def do_action(self, name, *args, **kwargs):
        method = getattr(self, name)
        self.args = args
        self.kwargs = kwargs

        data = ControllerData()
        self.before_action(data)
        method(data)
        self.after_action(data)
        return data

    def before_action(self, data):
        pass

    def after_action(self, data):
        pass
