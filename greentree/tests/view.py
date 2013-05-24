from greentree import View
from greentree.error import MissingMethodImplementationError
from greentree.tests.base import BaseTest


class ViewTest(BaseTest):

    def test_create_layout_error(self):
        def create_test_view():
            class TestView(View):
                pass
        #----------------------------------------------------------------------
        self.assertRaises(MissingMethodImplementationError, create_test_view)

    def test_create_layout_sucess(self):
        def create_test_view():
            class TestView2(View):

                def create_design(self):
                    pass
            TestView2(None)
            return True
        #----------------------------------------------------------------------
        self.assertTrue(create_test_view())

    def test_name(self):
        class TestView3(View):

            def create_design(self):
                pass
        #----------------------------------------------------------------------
        view = TestView3(None)

        self.assertEqual('TestView3', view.name())

    def test_init(self):
        class TestBinder(object):
            pass

        class TestView4(View):

            def create_design(self):
                pass
        #----------------------------------------------------------------------
        binder = TestBinder()
        view = TestView4(binder)

        self.assertEqual(binder, view.binder)
        self.assertTrue(view.signals['hide'] == [view.hide,])
        self.assertTrue(view.signals['show'] == [view.show,])
