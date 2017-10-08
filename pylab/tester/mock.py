"""@package mock
@brief  Mock test this tester framework.
@author Marcel H
@date   2017

@parblock
@b Classes
@li N/A

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

from random import randint
from . import TestPackage, TestScenario, BaseTestCase, PerfTestCase

def func(var):
    """Returns the function x^2"""
    return var * var


class MockTestPackage(TestPackage):
    """Mock test package for testing mock function."""

    def get_test_input_size(self):
        """Get random size"""
        return randint(1, 3)

    def create_test_input(self, scenario, size=None):
        """Creates the test input for mock function"""
        if scenario == TestScenario.BEST:
            return randint(1, 9)
        elif scenario == TestScenario.AVERAGE:
            return randint(10, 99) if size == 2 else randint(100, 999)
        else:
            return randint(900, 999)

    def get_expected_result(self, testInput):
        return testInput * testInput

    def verify(self, testInput, testOutput):
        assert self.get_expected_result(testInput) == testOutput


class MockTestCase(BaseTestCase):
    """Mock test case"""

    def setUp(self):
        super().setUp()
        self.object_under_test = func

    def test_method(self):
        """Method test"""
        testpkg = MockTestPackage()
        for i in range(100):
            with self.subTest(iter=i):
                self.execute(testpkg, self.object_under_test)


class MockPerfCase(PerfTestCase):
    """Mock performance test case"""

    def setUp(self):
        super().setUp()
        self.object_under_test = func

    def test_method(self):
        """Method test"""
        self.execute(MockTestPackage(), self.object_under_test)


if __name__ == '__main__':
    pass
