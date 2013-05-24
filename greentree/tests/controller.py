from greentree import Controller, ControllerData
from greentree.error import NoViewSelected

from .base import BaseTest


class ControllerDataTest(BaseTest):

    def test_init(self):
        cd = ControllerData()
        self.assertEqual({}, cd.binder_signals)
        self.assertEqual({}, cd.view_signals)
        self.assertEqual(None, cd.selected_view)

    def test_adding_binder_signals(self):
        signal_name = 'signal_name'
        arg1 = 'no name arg'

        cd = ControllerData()
        cd.add_binder_signal(signal_name, arg1)

        self.assertTrue(signal_name in cd.binder_signals)
        self.assertEqual(((arg1,), {}), cd.binder_signals[signal_name])

    def test_adding_view_signals(self):
        view_name = 'view name'
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        cd = ControllerData()
        cd.add_view_signal(view_name, signal_name, arg1, kwarg1=kwarg1)

        self.assertTrue(view_name in cd.view_signals)
        self.assertTrue(signal_name in cd.view_signals[view_name])
        self.assertEqual(((arg1,), {'kwarg1': kwarg1}), cd.view_signals[
                         view_name][signal_name])

    def test_view_select(self):
        view_name = 'view name'
        cd = ControllerData()
        cd.view_select(view_name)

        self.assertEqual(view_name, cd.selected_view)

    def test_view_select_with_hide_rest(self):
        view_name = 'view name'
        cd = ControllerData()
        cd.view_select(view_name, True)

        self.assertEqual(view_name, cd.selected_view)
        self.assertTrue('hide_all' in cd.binder_signals)
        self.assertEqual(((view_name,), {}), cd.binder_signals['hide_all'])

    def test_signal_view(self):
        view_name = 'view name'
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        cd = ControllerData()
        cd.view_select(view_name)
        cd.signal_view(signal_name, arg1, kwarg1=kwarg1)

        self.assertTrue(view_name in cd.view_signals)
        self.assertTrue(signal_name in cd.view_signals[view_name])
        self.assertEqual(((arg1,), {'kwarg1': kwarg1}), cd.view_signals[
                         view_name][signal_name])

    def test_signal_view_no_view_selected(self):
        signal_name = 'signal_name'
        arg1 = 'no name arg'
        kwarg1 = 'named arg'

        cd = ControllerData()
        self.assertRaises(
            NoViewSelected, cd.signal_view, signal_name, arg1, kwarg1=kwarg1)


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

