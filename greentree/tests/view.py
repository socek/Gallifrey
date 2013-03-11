from greentree import View
from greentree.tests.base import BaseTest
from greentree.error import MissingMethodImplementationError


class ViewTest(BaseTest):

    def test_create_layout_error(self):
        def create_test_view():
            class TestView(View):
                pass
        #-----------------------------------------------------------------------)
        self.assertRaises(MissingMethodImplementationError, create_test_view)

    def test_create_layout_sucess(self):
        def create_test_view():
            class TestView2(View):
                def create_design(self):
                    pass
            TestView2()
            return True
        #-----------------------------------------------------------------------)
        self.assertTrue(create_test_view())

    def test_connecting_signals(self):
        class TestView(View):
            def create_design(self):
                pass

            def connect_signals(self):
                self.test = True

        view = TestView()
        self.assertTrue(view.test)
