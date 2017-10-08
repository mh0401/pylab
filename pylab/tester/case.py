"""@package case
@brief  Test case extension
@author Marcel H
@date   2017

@parblock
@b Classes
@li TestPackage   Base test method class to encapsulate variations in test methods.
@li BaseTestCase  Base test case to be subclassed for implementation.
@li PerfTestCase  Performance test case to be subclassed for implementation.

@b Functions
@li N/A

@b Exceptions
@li N/A
@endparblock

@copyright Copyright (c) 2017 Marcel H

 MIT License
 
 Copyright (c) 2017 mh0401
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.

"""
from abc import ABC, abstractmethod
from unittest import TestCase
from time import time

from . import PerfData, Verbosity, TestScenario, Traceable, \
              assert_type, assert_cond, fullobjname, typename, \
              TestFailError

###########################


class TestPackage(ABC):
    """The purpose of this class is to encapsulate all the information for a test,
    e.g. scenarios, parameters, etc. Since every test method can be considered
    a different test, then this class may be derived for every test method
    in a test case class.
    Note that there is no type checking on the user input.
    Each test is responsible to generate the correct type for the code under test.
    """

    # TODO: Figure out a way to provide checking method (present debug info and halting the test).

    @classmethod
    def __subclasshook__(cls, C):
        if cls is TestPackage:
            if any("_generate" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    def __init__(self, userTestInput=None):
        """Initialize test method. Option to add user specific input for flexibility.
        The purpose may be to replicate a failing case (repeatability).
        @param  userTestInput   User test input (must be a list)
        """
        self.__usertestinput = None
        if userTestInput is not None:
            assert_type(userTestInput, list)
            self.__usertestinput = userTestInput

    @property
    def user_test_input(self):
        '''Returns the user specified test input'''
        return self.__usertestinput

    @abstractmethod
    def get_test_input_size(self):
        """Get the size of the desired test input."""

    @abstractmethod
    def create_test_input(self, scenario, size=None):
        """Create a single test input.
        @param  scenario   Desired test scenario. TestScenario enumeration class.
        @param  size       Size of the desired test input. If None, it will be random.
        @return            Input of the code under test.
        """

    @abstractmethod
    def get_expected_result(self, testInput):
        """Get expected result given the test input.
        @param  testInput  The test input used for the code under test.
        @return            The expected (correct) result.
        """

    @abstractmethod
    def verify(self, testInput, testOutput):
        """Verify the test output. Throws an error when test failed.
        @param   testInput  The test input used for the code under test.
        @param   testOutput The test output from the code under test ran w/ testInput.
        @throw   AssertionError
        """

    def get_test_input(self, scenario, size):
        """Get the test input to run for the test.
        It will use user test input if specified.
        If not, create the test input.
        @param  scenario   Desired test scenario to be created.
                           TestScenario enumeration class.
        @param  size       Desired test input size.
        @return            The test input for the code under test.
        """
        assert_type(scenario, TestScenario)
        if (self.user_test_input is not None and
            not isinstance(self.user_test_input, str) and
            len(self.user_test_input) > 0):
            return self.user_test_input.pop()
        else:
            return self.create_test_input(scenario, size)

    @staticmethod
    def assert_equal(var1, var2, msg=None):
        """Asserts whether two parameters are equal.
        Returns failure information for debugging.
        @param  var1   First parameter
        @param  var2   Second parameter
        @param  msg    Additional information (default: None)
        @throw  TestFailError
        """
        if var1 != var2:
            raise TestFailError('\n{}\n{} is not equal to {}'.format(
                '' if msg is None else msg, var1, var2))


class BaseTestCase(TestCase, Traceable):
    """Base test case for implementation class.
    Sub-class needs to define setUp() method to declare object under test and
    declare the test package object in the test method.
    """

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        Traceable.__init__(self)

        # We use attribute for this instead of passing a parameter
        # because we don't want duplication in case there are multiple methods.
        self.__object_under_test = None

        # To guarantee preservation of the original test input,
        # in case the object under test alters the test input.
        # Subclass can use this if necessary.
        self._testinputcopy = None

    @property
    def object_under_test(self):
        """Returns the object under test."""
        return self.__object_under_test

    @object_under_test.setter
    def object_under_test(self, obj):
        """Sets the object under test."""
        if self.object_under_test is None:
            self.__object_under_test = obj

    def tearDown(self):
        """Destroy test components."""
        super().tearDown()
        self.print_tr('Test finished. Destroy unnecessary objects', Verbosity.INFO)
        if self.object_under_test is not None:
            del self.__object_under_test

    def execute(self, testpkg, testcode):
        """Execute the test package against the test code.
        Throws an error when expected is not equal to actual data.
        @param  testpkg   Implementation class for TestPackage.
        @param  testcode  Code under test.
        @throw  AssertionError
        """
        self._pre_execute(testpkg, testcode)
        self._execute(testpkg, testcode)
        self._post_execute(testpkg, testcode)

    ## @protected
    def _pre_test(self, *args, **kwargs):
        """Interpose function prior to running the actual test.
        @param  args    List of arguments
        @param  kwargs  Keyword list of arguments
        """

    ## @protected
    def _post_test(self, *args, **kwargs):
        """Interpose function after running the test.
        @param  args    List of arguments
        @param  kwargs  Keyword list of arguments
        """

    ## @protected
    def _pre_execute(self, testpkg, testcode):
        """Interpose function prior to execution of test.
        Perform type checking.
        @param  testpkg   Implementation class for TestPackage.
        @param  testcode  Code under test.
        @throw  AssertionError
        """
        self.print_tr('Start pre-execute', Verbosity.DEBUG)
        assert_cond(testpkg is not None and testcode is not None,
                    AssertionError('Test code and package must not be None.'))
        assert_type(testpkg, TestPackage)
        assert_cond(hasattr(testcode, '__call__'),
                    AssertionError('{} is not callable'.format(testcode.__name__)))

    ## @protected
    def _post_execute(self, testpkg, testcode):
        """Interpose function after execution of test has completed.
        @param  testpkg   Implementation class for TestPackage.
        @param  testcode  Code under test.
        """

    ## @protected
    def _execute_loop(self, testpkg, testobj, repetition):
        """Execute the test X times.
        @param  testpkg     The test package object.
        @param  testobj     The code under test object.
        @param  repetition  The number of executions.
        """
        for i in range(repetition):
            with self.subTest(iter=i):
                self.execute(testpkg, testobj)

    ## @protected
    def _execute(self, testpkg, testcode):
        """Generate scenario, run the test method specified, and verify the data.
        Throws an error when expected is not equal to actual data.
        @param  testpkg   Implementation class for TestPackage.
        @param  testcode  Code under test.
        @throw  AssertionError
        """
        # Generate single test input given scenario.
        self.print_tr('Generating test inputs from scenarios.', Verbosity.DEBUG)
        testInput = testpkg.get_test_input(TestScenario.AVERAGE, testpkg.get_test_input_size())

        # Execute pre-test.
        self.print_tr('Execute pre-test.', Verbosity.DEBUG)
        self._pre_test(testInput)

        # Execute the code with the generated test input.
        self.print_tr('Execute code under test with the test input.', Verbosity.DEBUG)
        testOutput = None

        try:
            testOutput = testcode(testInput) # pylint: disable=not-callable
        except TypeError:
            testOutput = testcode(*testInput)  # pylint: disable=not-callable

        # Execute post-test.
        self.print_tr('Execute post-test.', Verbosity.DEBUG)
        self._post_test(testInput, testOutput)

        # Verify
        self.print_tr('Verifying test outputs', Verbosity.DEBUG)
        testpkg.verify(testInput if self._testinputcopy is None else self._testinputcopy,
                       testOutput)


class PerfTestCase(BaseTestCase):
    """Class encapsulating tests for measuring performance (time)."""

    ## @static
    SCENARIOS = (TestScenario.BEST, TestScenario.AVERAGE, TestScenario.WORST)
    SIZES = (10, 100, 500, 1000, 2000, 4000, 8000)

    def __init__(self, methodName='runTest'):
        """Constructor"""
        super().__init__(methodName)
        self.__perfdata = PerfData(typename(self))
        self.__testtime = None

    @staticmethod
    def runs(size):
        """Determine the number of runs given the size of the input.
        @param  size  The test input size.
        @return       The number of runs/executions.
        """
        return 100 if size <= 100 else (50 if size < 4000 else 10)

    ## @protected
    def _pre_test(self, *args, **kwargs): #@UnusedVariable
        """Interpose function prior to running the actual test.
        In this case, it is recording the start time.
        @param  args    List of arguments
        @param  kwargs  Keyword list of arguments
        """
        self.__testtime = time()

    ## @protected
    def _post_test(self, *args, **kwargs): #@UnusedVariable
        """Interpose function after running the test.
        In this case, it is calculating the execution time.
        @param  args    List of arguments
        @param  kwargs  Keyword list of arguments
        """
        self.__testtime = time() - self.__testtime

    ## @protected
    def _post_execute(self, testpkg, testcode): #@UnusedVariable
        """Interpose function after execution of test has completed.
        Report and plot the performance data.
        @param  testpkg   Implementation class for TestPackage.
        @param  testcode  Code under test.
        """
        self.__perfdata.codeundertest = fullobjname(testcode)
        self.__perfdata.report()
        self.__perfdata.plot()

    def _execute(self, testpkg, testcode):
        """Generate scenario, run the test method specified, and verify the data.
        Throws an error when expected is not equal to actual data.
        @param  testpkg   Implementation class for TestPackage.
        @param  testcode  Code under test.
        @throw  AssertionError
        """
        # Generate all scenarios/test inputs.
        for size in self.SIZES:
            for idxrun in range(self.runs(size)): #@UnusedVariable
                for scenario in self.SCENARIOS:
                    super()._execute(testpkg, testcode)
                    self.__perfdata.add(scenario, size, self.__testtime)
