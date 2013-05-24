from PySide.QtCore import Qt, Signal, Slot
from PySide.QtGui import QWidget
from .error import MissingMethodImplementationError


class ViewType(type(Qt), type):

    main_class = 'greentree.view.View'

    def __init__(cls, name, bases, dct):
        def check_if_methods_are_implemented(methods_name):
            for name in methods_name:
                if not hasattr(cls, name):
                    raise MissingMethodImplementationError(cls, name)
        #----------------------------------------------------------------------
        super(ViewType, cls).__init__(name, bases, dct)
        classfullname = '%s.%s' % (cls.__module__, cls.__name__)
        if classfullname != ViewType.main_class:
            check_if_methods_are_implemented(['create_design'])


class View(QWidget):

    __metaclass__ = ViewType

    mainsignal = Signal(object, object)

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.signals = {}
        self.mainsignal.connect(self.on_mainsignal)

        self.create_design()
        self.generate_signals()
        self.connect_qt_signals()

    @Slot()
    def on_mainsignal(self, signal, args):
        for method in self.signals[signal]:
            method(*args[0], **args[1])

    def add_signal(self, name, method):
        if name not in self.signals:
            self.signals[name] = []
        self.signals[name].append(method)

    def gtemit(self, signal, *args, **kwargs):
        self.mainsignal.emit(signal, (args, kwargs))

    def generate_signals(self):
        self.add_signal('show', self.show)
        self.add_signal('hide', self.hide)

    def connect_qt_signals(self):
        pass
