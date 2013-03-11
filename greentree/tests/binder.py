from PySide.QtCore import Signal
from greentree import Binder, Controller, View, ControllerData
from greentree.tests.base import BaseTest
from greentree.error import MissingMethodImplementationError

view_name = 'someviewname'


class TestController(Controller):
    def do_something(self, *args):
        data = ControllerData()
        data.add_binder_signal('sig', *args)
        return data

    def do_something_view(self, *args):
        data = ControllerData()
        data.add_view_signal(view_name, 'sig2', *args)
        return data


class TestView(View):
    sig2 = Signal((object,))

    def create_design(self):
        pass

    def connect_signals(self):
        self.sig2.connect(self.do_something)

    def do_something(self, *args):
        self.test2 = args

controller = TestController()


class BinderTest(BaseTest):

    def test_create_controller_error(self):
        def create_test_binder():
            class TestBinder(Binder):
                pass
        #-----------------------------------------------------------------------)
        self.assertRaises(MissingMethodImplementationError, create_test_binder)
        try:
            create_test_binder()
        except MissingMethodImplementationError, er:
            self.assertEqual("<class 'greentree.tests.binder.TestBinder'> create_controller", str(er))

    def test_smallest_binder(self):
        class TestBinder(Binder):
            def create_controller(self):
                return controller

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertEqual({}, binder.views)
        self.assertEqual(controller, binder.controller)

    def test_connect_signals(self):
        class TestBinder(Binder):
            def create_controller(self):
                return controller

            def connect_signals(self):
                self.test = True

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertEqual({}, binder.views)
        self.assertEqual(controller, binder.controller)
        self.assertTrue(controller, binder.test)

    def test_generate_views(self):
        class TestBinder(Binder):
            def create_controller(self):
                return controller

            def generate_views(self):
                self.add_view(view_name, TestView)

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertEqual(controller, binder.controller)
        self.assertTrue(view_name in binder.views)
        self.assertEqual(TestView, type(binder.views[view_name]))

    def test_binder_signals(self):
        class TestBinder(Binder):
            sig = Signal((object,))

            def create_controller(self):
                return controller

            def connect_signals(self):
                self.sig.connect(self.on_sig)

            def on_sig(self, *args):
                self.test = args

        binder = TestBinder()
        arg = 'arg'
        binder.make_controller_action('do_something', arg)
        self.assertEqual((arg,), binder.test)

    def test_views_signals(self):
        class TestBinder(Binder):
            def create_controller(self):
                return controller

            def generate_views(self):
                self.add_view(view_name, TestView)

        binder = TestBinder()
        arg = 'arg'
        binder.make_controller_action('do_something_view', arg)
        self.assertEqual((arg,), binder.views[view_name].test2)
