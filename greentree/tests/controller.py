from greentree import Controller
from greentree.error import NoViewSelected

from .base import BaseTest


class ControllerTest(BaseTest):

    class TestController(Controller):

        def __init__(self, *args, **kwargs):
            super(type(self), self).__init__(*args, **kwargs)
            self._before = False
            self._after = False

        def before_action(self):
            self._before = True

        def myaction(self, arg1=None, kwarg2=None):
            tester = self.args[0]
            tester.assertTrue(self._before)

            tester.assertFalse(self._after)

        def after_action(self):
            self._after = True

    def test_init(self):
        ctrl = self.TestController()

        self.assertFalse(ctrl._before)
        self.assertFalse(ctrl._after)
        self.assertEqual([], ctrl.signals)
        self.assertEqual([], ctrl.signals_end)
        self.assertEqual(None, ctrl.selected_view)

    def test_do_action(self):
        ctrl = self.TestController()

        kwarg2 = 2

        ctrl.do_action('myaction', self, kwarg2=kwarg2)

        self.assertTrue(ctrl._before)
        self.assertTrue(ctrl._after)
        self.assertEqual((self,), ctrl.args)
        self.assertEqual({'kwarg2': kwarg2}, ctrl.kwargs)

    def test_add_view_signal(self):
        ctrl = self.TestController()
        ctrl.add_view_signal('view_name', 'signal_name', 1, arg2=2)

        self.assertEqual(1, len(ctrl.signals))
        signal = ctrl.signals[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual('view_name', signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_add_view_signal_at_end(self):
        ctrl = self.TestController()
        ctrl.add_view_signal_at_end('view_name', 'signal_name', 1, arg2=2)

        self.assertEqual(1, len(ctrl.signals_end))
        signal = ctrl.signals_end[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual('view_name', signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_add_binder_signal(self):
        ctrl = self.TestController()
        ctrl.add_binder_signal('signal_name', 1, arg2=2)

        self.assertEqual(1, len(ctrl.signals))
        signal = ctrl.signals[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual(None, signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_add_binder_signal_at_end(self):
        ctrl = self.TestController()
        ctrl.add_binder_signal_at_end('signal_name', 1, arg2=2)

        self.assertEqual(1, len(ctrl.signals_end))
        signal = ctrl.signals_end[0]
        self.assertEqual('signal_name', signal.name)
        self.assertEqual(None, signal.view_name)
        self.assertEqual(((1,), {'arg2': 2}), signal.args)

    def test_select_view(self):
        view_name = 'view name'
        ctrl = self.TestController()
        ctrl.select_view(view_name)

        self.assertEqual(view_name, ctrl.selected_view)

    def test_select_view_with_hide_rest(self):
        view_name = 'view name'
        ctrl = self.TestController()
        ctrl.select_view(view_name, True)

        self.assertEqual(view_name, ctrl.selected_view)
        self.assertEqual(1, len(ctrl.signals_end))
        signal = ctrl.signals_end[0]
        self.assertEqual('hide_all', signal.name)
        self.assertEqual(None, signal.view_name)
        self.assertEqual(((view_name,), {}), signal.args)

    def test_add_signal(self):
        view_name = 'view name'
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        ctrl = self.TestController()
        ctrl.select_view(view_name)
        ctrl.add_signal(signal_name, arg1, kwarg1=kwarg1)

        self.assertEqual(1, len(ctrl.signals))
        signal = ctrl.signals[0]
        self.assertEqual(signal_name, signal.name)
        self.assertEqual(view_name, signal.view_name)
        self.assertEqual(((arg1,), {'kwarg1': kwarg1}), signal.args)

    def test_add_signal_no_view_selected(self):
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        ctrl = self.TestController()
        self.assertRaises(
            NoViewSelected, ctrl.add_signal, signal_name, arg1, kwarg1=kwarg1)

    def test_get_signals(self):
        ctrl = self.TestController()
        ctrl.add_binder_signal('name1')
        ctrl.add_binder_signal('name2')
        ctrl.add_binder_signal_at_end('name3')
        ctrl.add_binder_signal_at_end('name4')

        signals = ctrl.get_signals()
        signal_names = [signal.name for signal in signals]

        self.assertEqual(['name1', 'name2', 'name4', 'name3'], signal_names)
