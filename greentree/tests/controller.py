from greentree import Controller, ControllerData
from .base import BaseTest

class ControllerDataTest(BaseTest):

    def test_adding_binder_signals(self):
        signal_name = 'signal_name'
        arg1 = 'no name arg'

        cd = ControllerData()
        cd.add_binder_signal(signal_name, arg1)

        self.assertTrue(signal_name in cd.binder_signals)
        self.assertEqual((arg1,), cd.binder_signals[signal_name])

    def test_adding_view_signals(self):
        view_name = 'view name'
        signal_name = 'signal_name'
        arg1 = 'no name arg'

        cd = ControllerData()
        cd.add_view_signal(view_name, signal_name, arg1)

        self.assertTrue(view_name in cd.view_signals)
        self.assertTrue(signal_name in cd.view_signals[view_name])
        self.assertEqual((arg1,), cd.view_signals[view_name][signal_name])

class ControllerTest(BaseTest):

    def test_bare_controller(self):
        class TestController(Controller):
            pass
        ctrl = TestController()

        before_show_data = ctrl.before_show()
        self.assertEqual({}, before_show_data.binder_signals)
        self.assertEqual({}, before_show_data.view_signals)

        before_show_data = ctrl.after_show()
        self.assertEqual({}, before_show_data.binder_signals)
        self.assertEqual({}, before_show_data.view_signals)
