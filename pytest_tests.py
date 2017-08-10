import logging
import pytest
import sys

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level='INFO')


class TestPyTest:
    @pytest.fixture(scope='class')
    def test_list(self):
        """
        This is a fixture function whose scope is the class. This means that this function
        will be executed only once for this class. It will be executed before any test functions are executed.

        This function also has some teardown code. All code after the yield statement serves as the teardown code which
        will be executed only once after all test functions have finished executing.

        :return: A fixture object that can be passed as an input to test functions. This specific fixture function
                 returns a list of string values.
        """
        logging.info('Inside class setup...')
        t_list = ['Ontario', 'Sasketchewan', 'Nova Scotia', 'New Brunswick', 'Newfoundland and Labrador',
                  'British Columbia', 'Alberta', 'Quebec', 'Manitoba', 'Prince Edward Island',
                  'Northwest Territories', 'Yukon', 'Nunavut']
        yield t_list
        logging.info('Class teardown.')

    def test_one(self):
        """
        A simple test that does nothing.
        """
        assert True

    def test_two(self, test_list):
        """
        This test function takes a fixture object as an input argument. In this case, the test_list fixture function
        defined above provides the fixture object.
        :param test_list: provided by the fixture function with the same name defined above.
        """
        assert 'Nova Scotia' in test_list

    @pytest.mark.parametrize('item', ['Ontario', 'New Brunswick', 'Sasketchewan'])
    def test_three(self, test_list, item):
        """
        This is an example of a parametrized test.
        Parameters are passed through pytest's builtin pytest.mark.parametrize decorator.

        :param test_list: provided by the fixture object with the same name.
        :param item: provided by the @parametrize decorator. In this case, the decorator provides three different
                    parameters which means that this test will run three times in total.

        """
        assert item in test_list

    @pytest.mark.xfail(reason='Testing the @xfail decorator.')
    def test_four(self):
        """
        This is a test that is expected to fail. Commonly used when the test is for a feature
        that is not yet implemented or a bug that is not yet fixed.
        Such a test will be run but will not be marked as a failure. Instead, it'll be reported
        in a separate section called XFAIL (expected to fail.)

        The following statement will return a ZeroDivisionError but will be reported as XFAIL
        because of the @xfail decorator.
        """
        1 / 0

    @pytest.mark.xfail(raises=AssertionError, reason='Testing the @xfail decorator for a specific exception.')
    def test_five(self, test_list):
        """
        This is another example of an @xfail but, unlike test_four(), this test will be marked as XFAIL only if
        it raises an AssertionError. For any other exception, it will be reported as a regular failure.
        :param test_list: provide by the fixture function with the same name.
        """
        assert 'California' in test_list

    @pytest.mark.parametrize('item',
                             ['Ontario',
                              pytest.param('New York', marks=pytest.mark.xfail(reason='testing xfail')),
                              'Sasketchewan'])
    def test_six(self, test_list, item):
        """
        Another way to use the xfail decorator. Here, the test will executed three times once with each of the
        input parameters but is expected to fail for only one of the inputs.
        :param test_list: provided by the fixture function with the same name.
        :param item: provided by the @parametrize decorator
        """
        assert item in test_list
        
    @pytest.mark.skip(reason='Testing the @skip decorator.')
    def test_seven(self):
        """
        This test will be skipped because it has been marked with the @skip decorator.
        This test will be reported in a separate section called SKIPPED.
        """
        assert True
        
    @pytest.mark.skipif(sys.platform == 'win32',
                        reason='Testing the @skipif decorator')
    def test_eight(self):
        """
        This test will be executed only if sys.platform is not win32; will be skipped otherwise.
        """
        assert True
        
    def test_nine(self):
        """
        Skipping a test without the decorator can be accomplished
        by calling the pytest.skip(reason) function from inside the test method.
        """
        if sys.platform == 'win32':
            pytest.skip('Unsupported platform. Therefore, skipping the test.')
        assert True
