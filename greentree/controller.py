from PySide.QtCore import QObject


class ControllerData(object):
    def __init__(self):
        self.binder_signals = {}
        self.view_signals = {}

    def add_binder_signal(self, signal_name, *args, **kwargs):
        self.binder_signals[signal_name] = (args, kwargs)

    def add_view_signal(self, view_name, signal_name, *args, **kwargs):
        if not view_name in self.view_signals:
            self.view_signals[view_name] = {}
        self.view_signals[view_name][signal_name] = (args, kwargs)


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent=parent)

    def before_show(self):
        return ControllerData()

    def after_show(self):
        return ControllerData()
