from PySide.QtCore import Slot, Signal


class SignalReadyMixin(object):

    mainsignal = Signal(object, object)

    def signals_init(self):
        self.signals = {}
        self.mainsignal.connect(self._mainsignal)
        self.generate_signals()

    @Slot()
    def _mainsignal(self, signal, args):
        for method in self.signals[signal]:
            method(*args[0], **args[1])

    def add_signal(self, method, name=None):
        if name is None:
            name = method.__name__
        if name not in self.signals:
            self.signals[name] = []
        self.signals[name].append(method)

    def gtemit(self, signal, *args, **kwargs):
        self.mainsignal.emit(signal, (args, kwargs))

    def generate_signals(self):
        pass
