from greentree import Binder, Controller, View
from greentree.tests.base import BaseTest
from greentree.error import MissingMethodImplementationError

view_name = 'TestView'


class TestController(Controller):

    def do_something(self, data):
        data.add_binder_signal('sig', *self.args)

    def do_something_view(self, data):
        data.add_view_signal(view_name, 'sig2', *self.args)


class TestView(View):

    def __init__(self, *args, **kwargs):
        super(TestView, self).__init__(*args, **kwargs)
        self._hide = False
        self._show = False

    def create_design(self):
        pass

    def generate_signals(self):
        super(TestView, self).generate_signals()
        self.add_signal('sig2', self.do_something)

    def do_something(self, *args):
        self.test2 = args

    def hide(self):
        self._hide = True


class TestViewSecond(View):

    def __init__(self, *args, **kwargs):
        super(TestViewSecond, self).__init__(*args, **kwargs)
        self._hide = False
        self._show = False

    def create_design(self):
        pass

    def hide(self):
        self._hide = True

    def show(self):
        self._show = True

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
            self.assertEqual(
                "<class 'greentree.tests.binder.TestBinder'> create_controller", str(er))

    def test_smallest_binder(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertEqual({}, binder.views)
        self.assertEqual(controller, binder.controller)

    def test_generate_views(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

            def generate_views(self):
                self.add_view(TestView)

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertEqual(controller, binder.controller)
        self.assertTrue(view_name in binder.views)
        self.assertEqual(TestView, type(binder.views[view_name]))

    def test_binder_signals(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

            def generate_signals(self):
                self.add_signal('sig', self.sig)

            def sig(self, *args):
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
                self.add_view(TestView)

        binder = TestBinder()
        arg = 'arg'
        binder.make_controller_action('do_something_view', arg)
        self.assertEqual((arg,), binder.views[view_name].test2)

    def test_init(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

            def generate_views(self):
                self.add_view(TestView)

            def add_all_views_to_layout(self, layout):
                self.test_add_all_views_to_layout = True

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertTrue(type(binder.views['TestView']) == TestView)
        self.assertEqual(controller, binder.controller)
        self.assertEqual([binder.hide_all, ], binder.signals['hide_all'])
        self.assertTrue(binder.test_add_all_views_to_layout)

    def test_hide_all(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

            def generate_views(self):
                self.add_view(TestView)
                self.add_view(TestViewSecond)

        binder = TestBinder()
        binder.hide_all()

        self.assertTrue(binder.views['TestView']._hide)
        self.assertTrue(binder.views['TestViewSecond']._hide)

        self.assertFalse(binder.views['TestView']._show)
        self.assertFalse(binder.views['TestViewSecond']._show)

    def test_hide_all_with_exception_name(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

            def generate_views(self):
                self.add_view(TestView)
                self.add_view(TestViewSecond)

        binder = TestBinder()
        binder.hide_all('TestViewSecond')

        self.assertTrue(binder.views['TestView']._hide)
        self.assertFalse(binder.views['TestViewSecond']._hide)

        self.assertFalse(binder.views['TestView']._show)
        self.assertTrue(binder.views['TestViewSecond']._show)
