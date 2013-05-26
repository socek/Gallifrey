from greentree import Controller, ControllerData
from greentree.error import NoViewSelected

from .base import BaseTest


class ControllerDataTest(BaseTest):

    def test_init(self):
        cd = ControllerData()
        self.assertEqual([], cd.signals)
        self.assertEqual([], cd.signals_end)
        self.assertEqual(None, cd.selected_view)

    def test_add_view_signal(self):
        cd = ControllerData()
        cd.add_view_signal('view_name', 'signal_name', 1, arg2=2)

        self.assertEqual(1, len(cd.signals))
        signal = cd.signals[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual('view_name', signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_add_view_signal_at_end(self):
        cd = ControllerData()
        cd.add_view_signal_at_end('view_name', 'signal_name', 1, arg2=2)

        self.assertEqual(1, len(cd.signals_end))
        signal = cd.signals_end[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual('view_name', signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_add_binder_signal(self):
        cd = ControllerData()
        cd.add_binder_signal('signal_name', 1, arg2=2)

        self.assertEqual(1, len(cd.signals))
        signal = cd.signals[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual(None, signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_add_binder_signal_at_end(self):
        cd = ControllerData()
        cd.add_binder_signal_at_end('signal_name', 1, arg2=2)

        self.assertEqual(1, len(cd.signals_end))
        signal = cd.signals_end[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual(None, signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_select_view(self):
        view_name = 'view name'
        cd = ControllerData()
        cd.select_view(view_name)

        self.assertEqual(view_name, cd.selected_view)

    def test_select_view_with_hide_rest(self):
        view_name = 'view name'
        cd = ControllerData()
        cd.select_view(view_name, True)

        self.assertEqual(view_name, cd.selected_view)
        self.assertEqual(1, len(cd.signals_end))
        signal = cd.signals_end[0]
        self.assertEqual('hide_all', signal.name)
        self.assertEqual(None, signal.view_name)
        self.assertEqual(((view_name,), {}), signal.args)

    def test_add_signal(self):
        view_name = 'view name'
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        cd = ControllerData()
        cd.select_view(view_name)
        cd.add_signal(signal_name, arg1, kwarg1=kwarg1)

        self.assertEqual(1, len(cd.signals))
        signal = cd.signals[0]
        self.assertEqual(signal_name, signal.name)
        self.assertEqual(view_name, signal.view_name)
        self.assertEqual(((arg1,), {'kwarg1': kwarg1}), signal.args)

    def test_add_signal_no_view_selected(self):
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        cd = ControllerData()
        self.assertRaises(
            NoViewSelected, cd.add_signal, signal_name, arg1, kwarg1=kwarg1)

    def test_get_signals(self):
        cd = ControllerData()
        cd.add_binder_signal('name1')
        cd.add_binder_signal('name2')
        cd.add_binder_signal_at_end('name3')
        cd.add_binder_signal_at_end('name4')

        signals = cd.get_signals()
        signal_names = [signal.name for signal in signals]

        self.assertEqual(['name1', 'name2', 'name4', 'name3'], signal_names)


class ControllerTest(BaseTest):

    class TestController(Controller):

        def __init__(self, *args, **kwargs):
            super(type(self), self).__init__(*args, **kwargs)
            self._before = False
            self._after = False

        def before_action(self, data):
            data._before = True
            self._before = True
            data._after = False

        def myaction(self, data):
            tester = self.args[0]
            tester.assertTrue(data._before)
            tester.assertTrue(self._before)

            tester.assertFalse(data._after)
            tester.assertFalse(self._after)

        def after_action(self, data):
            data._after = True
            self._after = True

    def test_init(self):
        ctrl = self.TestController()

        self.assertFalse(ctrl._before)
        self.assertFalse(ctrl._after)

    def test_do_action(self):
        ctrl = self.TestController()

        kwarg2 = 2

        data = ctrl.do_action('myaction', self, kwarg2=kwarg2)

        self.assertTrue(data._before)
        self.assertTrue(ctrl._before)

        self.assertTrue(data._after)
        self.assertTrue(ctrl._after)

        self.assertEqual((self,), ctrl.args)
        self.assertEqual({'kwarg2': kwarg2}, ctrl.kwargs)
