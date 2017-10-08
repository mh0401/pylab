"""@package test_array
@brief      Test everything related to a 1-D list.
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@parblock
@b Classes
@li SortTestPackage        Test package for testing sort algorithms.
@li InversionTestPackage   Test package for testing inversions.
@li MaxsubarrayTestPackage Test package for testing maxsubarray.
@li ArrayTestCase          Test case class for testing all.

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
from random import randint, sample
from copy import deepcopy
from pylab import TestPackage, BaseTestCase, TestScenario, \
                    inversions_div, inversions_naive, maxsubarray_div, \
                    maxsubarray_div2, maxsubarray_linear, maxsubarray_naive, \
                    merge_sort

from . import NUMBER_OF_TEST_RUNS


class SortTestPackage(TestPackage):
    """Test package for combinatorics functions."""

    def __init__(self, userTestInput=None):
        """Constructor class.
        @param  userTestInput   Fixed test input provided by the user (directed test).
        """
        super().__init__(userTestInput)

    def get_test_input_size(self):
        """Returns the size of the array for combinations."""
        return randint(5, 1000)

    def create_test_input(self, scenario, size=None):
        """Create the test input for sort algorithm.
        @param  scenario  TestScenario enumeration type.
        @param  size      Size of the iterable (default: None)
        """
        lstinput = sample(range(-size, size), size)

        if scenario != TestScenario.AVERAGE:
            slst = sorted(lstinput)
            return slst if scenario == TestScenario.BEST else reversed(slst)
        return lstinput

    def get_expected_result(self, testInput):
        """Returns the sorted test input.
        @param   testInput  List of comparable elements.
        @return             Sorted test input.
        """
        return sorted(testInput)

    def verify(self, testInput, testOutput):
        """Verify/check sorting algorithm's output vs. expected output.
        @param  testInput   List input for the sorting algorithm.
        @param  testOutput  Sorted output from the code under test.
        """
        expOutput = self.get_expected_result(testInput)
        info = 'Input: {}, Size of input: {}\n\
Output: {}, Size of output: {}\nExpected: {}, Size of expected: {}'.format(
            testInput, len(testInput), testOutput, len(testOutput),
            expOutput, len(expOutput))

        # Test correct length
        self.assert_equal(len(expOutput), len(testOutput), info)

        # Test correct content
        self.assert_equal(expOutput, testOutput, info)


class InversionsTestPackage(SortTestPackage):
    """Test package for testing inversions algorithm."""

    def get_expected_result(self, testInput):
        """Returns the expected number of inversions exists in the test input.
        @param   testInput  List of comparable elements.
        @return             Expected number of inversions in test input.
        """
        return inversions_naive(testInput)

    def verify(self, testInput, testOutput):
        """Verify/check correct number of inversions.
        @param  testInput   List of comparable elements as test input.
        @param  testOutput  Actual number of inversions in test input.
        """
        expOutput = self.get_expected_result(testInput)
        info = 'Input: {}, Size of input: {}\nOutput: {}, \nExpected: {}'.format(
            testInput, len(testInput), testOutput, expOutput)

        # Test correct inversions
        self.assert_equal(expOutput, testOutput, info)


class MaxsubarrayTestPkg(SortTestPackage):
    """Test package for testing max-sub-array algorithm."""

    def get_expected_result(self, testInput):
        """Returns the expected max-sub-array of the test input.
        @param   testInput  List of summable elements.
        @return             Expected maxsubarray of the test input.
        """
        return maxsubarray_naive(testInput)

    def verify(self, testInput, testOutput):
        """Verify/check test input against test output.
        @param  testInput   List of summable elements.
        @param  testOutput  Actual maxsubarray of the test input.
        """
        expOutput = self.get_expected_result(testInput)
        info = 'Input: {}, Size of input: {}\nOutput: {}, \nExpected: {}'.format(
            testInput, len(testInput), testOutput, expOutput)

        # Test correct sum and the sum is indeed correct from test input
        self.assert_equal(expOutput[2], testOutput[2], info)
        self.assert_equal(expOutput[2], sum(testInput[testOutput[0]:testOutput[1] + 1]), info)


class ArrayTestCase(BaseTestCase):
    '''
    Test class providing test methods for algorithms involving lists.
    '''

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def setUp(self):
        super().setUp()
        self.object_under_test = None

    def _pre_test(self, *args, **kwargs): #@UnusedVariable
        """Copy test input since it may be altered by the object under test."""
        self._testinputcopy = deepcopy(*args) #pylint: disable=no-value-for-parameter

    def test_inversions_div(self):
        """Test inversions div algorithm."""
        testpkg = InversionsTestPackage()
        self._execute_loop(testpkg, inversions_div, NUMBER_OF_TEST_RUNS)

    def test_maxsubarray_div(self):
        """Test maxsubarray div algorithm"""
        self._execute_loop(MaxsubarrayTestPkg(), maxsubarray_div, NUMBER_OF_TEST_RUNS)

    def test_maxsubarray_div2(self):
        """Test maxsubarray div ver.2 algorithm."""
        self._execute_loop(MaxsubarrayTestPkg(), maxsubarray_div2, NUMBER_OF_TEST_RUNS)

    def test_maxsubarray_linear(self):
        """Test maxsubarray linear algorithm."""
        self._execute_loop(MaxsubarrayTestPkg(), maxsubarray_linear, NUMBER_OF_TEST_RUNS)

    def test_merge_sort(self):
        """Test sorting algorithm."""
        testpkg = SortTestPackage()
        self._execute_loop(testpkg, merge_sort, 1)
