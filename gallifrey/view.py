from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout, QProgressBar
from .error import MissingMethodImplementationError


class ViewType(type(Qt), type):

    main_class = 'gallifrey.view.View'

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


class LoadingBarView(View):

    def create_design(self):
        def create_loading_bar(lay):
            bar = QProgressBar()
            bar.setMaximum(0)
            bar.setTextVisible(False)
            bar.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(bar)
            return bar

        def create_layout():
            lay = QVBoxLayout(self)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setAlignment(Qt.AlignTop)
            return lay
        #-----------------------------------------------------------------------
        lay = create_layout()
        create_loading_bar(lay)
