"""@package test_combinatorics
@brief      Test combination and permutation
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@parblock
@b Classes
@li CombinatoricsTestPackage  Test package for combination/permutation
@li CombinatoricsTestCase     Test case class for testing both.

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
from typing import Generator
from itertools import combinations
from random import randint, sample
from pylab import BaseTestCase, TestPackage, n_combinations
from . import NUMBER_OF_TEST_RUNS


class CombinatoricsTestPackage(TestPackage):
    """Test package for combinatorics functions."""

    def __init__(self, userTestInput=None, function=combinations, nFunction=n_combinations):
        """Constructor class.
        @param  userTestInput   Fixed test input provided by the user (directed test).
        @param  nfunction       Function pointer for the size of combinatorics.
        """
        super().__init__(userTestInput)
        self.__counter = nFunction
        self.__generator = function

    def get_test_input_size(self):
        """Returns the size of the array for combinatorics."""
        # TODO: Push the limit of size on combinatorics test.
        # Size can't be too large.
        # Remember, its factorial, so it rises fast towards infinity.
        return randint(5, 10)

    def create_test_input(self, scenario, size=None): #@UnusedVariable
        """Create the test input for combinatorics.
        @param  scenario  TestScenario enumeration type.
        @param  size      Size of the iterable (default: None)
        """
        assert size is not None
        return sample(range(-size, size), size), randint(2, size)

    def get_expected_result(self, testInput):
        """Returns the expected/correct result given test input.
        @param   testInput  Tuple containing iterable/list with the amount to select.
        @return             All combinations from the test input.
        """
        return [x for x in self.__generator(*testInput)]

    def verify(self, testInput, testOutput):
        """Verify/check test input against test output.
        @param  testInput   Tuple input for the combination function (iterable and select).
        @param  testOutput  Actual output from the code under test.
        """
        result = None
        expOutput = self.get_expected_result(testInput)
        info = 'Input: {}, Size of input: {}\n\
Output: {}, Size of output: {}\nExpected: {}, Size of expected: {}'.format(
            testInput, len(testInput[0]), testOutput, len(testOutput),
            expOutput, len(expOutput))

        # Tests number of combination calculation
        self.assert_equal(len(expOutput),
                          self.__counter(len(testInput[0]), testInput[1]),
                          self.__counter.__name__ + ' failed.\n' + info)

        # Test correct length
        if isinstance(testOutput, Generator):
            result = [x for x in testOutput]
        else:
            result = testOutput
        self.assert_equal(len(expOutput), len(result), info)

        # Test correct content
        self.assert_equal(expOutput, result, info)


class CombinatoricsTestCase(BaseTestCase):
    '''
    Test class providing test methods for combinatorics functions.
    '''

    def setUp(self):
        super().setUp()
        # TODO: Update object under test with correct combinatoric functions.
        #self.object_under_test = (combination, permutation)
        self.object_under_test = combination

    def test_sanity(self):
        """Sanity check/Directed tests."""
        userInputs = [(['A', 'B', 'C', 'D', 'E'], 1), (['A', 'B', 'C', 'D', 'E'], 2),
                      (['A', 'B', 'C', 'D', 'E'], 5)]
        testpkgs = CombinatoricsTestPackage(userInputs)
        self._execute_loop(testpkgs, self.object_under_test, len(userInputs))
#        testpkgs = CombinationTestPackage(userInputs), PermutationTestPackage(userInputs)
#        for pkg, func in zip(testpkgs, self.object_under_test):
#            self._execute_loop(pkg, func, len(userInputs))

    def test_regress(self):
        """Regression with randomized inputs."""
        testpkgs = CombinatoricsTestPackage()
        self._execute_loop(testpkgs, self.object_under_test, NUMBER_OF_TEST_RUNS)
#        testpkgs = CombinationTestPackage(), PermutationTestPackage()
#        for pkg, func in zip(testpkgs, self.object_under_test):
#            self._execute_loop(pkg, func, NUMBER_OF_TEST_RUNS)
