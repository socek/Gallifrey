from greentree import Binder, Controller, View
from greentree.tests.base import BaseTest
from greentree.error import MissingMethodImplementationError
from mock import patch

view_name = 'TestView'


class TestController(Controller):

    def do_something(self, arg=None):
        self.add_binder_signal('sig', *self.args)

    def do_something_view(self, arg=None):
        self.add_view_signal(view_name, 'sig2', *self.args)


class TestView(View):

    def __init__(self, *args, **kwargs):
        super(TestView, self).__init__(*args, **kwargs)
        self._hide = False
        self._show = False

    def create_design(self):
        pass

    def generate_signals(self):
        super(TestView, self).generate_signals()
        self.add_signal(self.do_something, 'sig2')

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
                pass

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertEqual({}, binder.views)

    def test_generate_views(self):
        class TestBinder(Binder):

            def create_controller(self):
                pass

            def generate_views(self):
                self.add_view(TestView)

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertTrue(view_name in binder.views)
        self.assertEqual(TestView, type(binder.views[view_name]))

    def test_binder_signals(self):
        class TestBinder(Binder):

            def create_controller(self):
                return controller

            def generate_signals(self):
                self.add_signal(self.sig, 'sig')

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

            def generate_signals(self):
                self.add_signal(self.sig, 'sig')

            def sig(self, *args):
                self.test = args

            def generate_views(self):
                self.add_view(TestView)

        binder = TestBinder()
        arg = 'arg'
        binder.make_controller_action('do_something_view', arg)
        self.assertEqual((arg,), binder.views[view_name].test2)

    def test_init(self):
        class TestBinder(Binder):

            def create_controller(self):
                pass

            def generate_views(self):
                self.add_view(TestView)

            def add_all_views_to_layout(self, layout):
                self.test_add_all_views_to_layout = True

        binder = TestBinder()
        self.assertEqual(None, binder._parent)
        self.assertTrue(type(binder.views['TestView']) == TestView)
        self.assertEqual([binder.hide_all, ], binder.signals['hide_all'])
        self.assertTrue(binder.test_add_all_views_to_layout)

    def test_hide_all(self):
        class TestBinder(Binder):

            def create_controller(self):
                pass

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
                pass

            def generate_views(self):
                self.add_view(TestView)
                self.add_view(TestViewSecond)

        binder = TestBinder()
        binder.hide_all('TestViewSecond')

        self.assertTrue(binder.views['TestView']._hide)
        self.assertFalse(binder.views['TestViewSecond']._hide)

        self.assertFalse(binder.views['TestView']._show)
        self.assertTrue(binder.views['TestViewSecond']._show)

    def test_make_controller_action(self):
        class TestController2(Controller):

            def do_something(self):
                self.add_view_signal('TestView', 'signal_view', 1, kwarg2=2)
                self.add_binder_signal('signal', 3, kwarg2=4)

        class TestView(View):

            def __init__(self, *args, **kwargs):
                super(TestView, self).__init__(*args, **kwargs)
                self._hide = False
                self._show = False

            def create_design(self):
                pass

            def gtemit(self, signal, *args, **kwargs):
                self.signal = signal
                self.args = args
                self.kwargs = kwargs

        class TestBinder(Binder):

            def create_controller(self):
                self._data = {}
                return TestController2()

            def generate_views(self):
                self.add_view(TestView)

            def gtemit(self, signal, *args, **kwargs):
                self.signal = signal
                self.args = args
                self.kwargs = kwargs

        binder = TestBinder()
        binder.make_controller_action('do_something')

        view = binder.views['TestView']
        self.assertEqual('signal_view', view.signal)
        self.assertEqual((1,), view.args)
        self.assertEqual({'kwarg2': 2}, view.kwargs)

        self.assertEqual('signal', binder.signal)
        self.assertEqual((3,), binder.args)
        self.assertEqual({'kwarg2': 4}, binder.kwargs)

    def test_visible_views(self):
        class TestBinder(Binder):

            def create_controller(self):
                pass

            def generate_views(self):
                self.add_view(TestView)
                self.add_view(TestViewSecond)

        binder = TestBinder()
        self.assertEqual([], binder.visible_views())

    def test_visible_views_after_hide_all(self):
        class TestBinder(Binder):

            def create_controller(self):
                pass

            def generate_views(self):
                self.add_view(TestView)
                self.add_view(TestViewSecond)

        def mock_show(self):
            self.showed = True

        def mock_hide(self):
            self.showed = False

        def mock_isVisible(self):
            try:
                return self.showed
            except AttributeError:
                return False

        binder = TestBinder()
        with patch.object(View, 'show', mock_show):
            with patch.object(View, 'hide', mock_hide):
                with patch.object(View, 'isVisible', mock_isVisible):
                    binder.hide_all('TestView')
                    excepted_data = [binder.views['TestView']]
                    self.assertEqual(excepted_data, binder.visible_views())
