from greentree.signals import SignalReadyMixin
from greentree.tests.base import BaseTest
from PySide.QtCore import QObject


signal_name = 'sig'


class Signal(QObject, SignalReadyMixin):
    pass


def testmethod(*args, **kwargs):
    pass


class SignalWithGenerator(QObject, SignalReadyMixin):

    def generate_signals(self):
        self.add_signal(signal_name, testmethod)


class SignalReadyMixinTest(BaseTest):

    def test_init(self):
        obj = Signal()
        obj.signals_init()
        self.assertEqual({}, obj.signals)

    def test_add_signal_once(self):
        obj = Signal()
        obj.signals_init()
        obj.add_signal(signal_name, testmethod)
        self.assertEqual([testmethod], obj.signals[signal_name])

    def test_add_signal_twice(self):
        obj = Signal()
        obj.signals_init()
        obj.add_signal(signal_name, testmethod)
        obj.add_signal(signal_name, testmethod)
        self.assertEqual([testmethod, testmethod], obj.signals[signal_name])

    def test_generate_signals(self):
        obj = SignalWithGenerator()
        obj.signals_init()
        self.assertEqual({signal_name: [testmethod]}, obj.signals)

    def test_emiting_signals(self):
        ret = {}
        def testmethod_2(*args, **kwargs):
            ret['args'] = args
            ret['kwargs'] = kwargs
        obj = SignalWithGenerator()
        obj.signals_init()
        obj.add_signal('sig2', testmethod_2)

        arg1 = 1
        arg2 = 2
        obj.gtemit('sig2', arg1, arg2=arg2)

        self.assertEqual((1,), ret['args'])
        self.assertEqual({'arg2': 2}, ret['kwargs'])

