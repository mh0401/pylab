'''
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

Created on Jul 18, 2017

@author: mh0401
'''
from time import time
from random import sample
from pylab import * #pylint: disable=wildcard-import


def __test(func, array):
    print("Func  : {0}".format(func.__name__))
    print("Input : {0}".format(array))
    print("Output: {0}".format(func(array)))
    print("Post  : {0}\n".format(array))


def __speed(func, *inputs):
    tstart = time()
    func(*inputs)
    tend = time()
    print('{}, size:{}, time: {}'.format(func.__name__, len(inputs), tend - tstart))


def main():
    """The main entry point"""
    __test(insertion_sort, [2, 3, 5, 6, 12, -1, -3, -2, 0])
    __test(selection_sort, [2, 32, 34, -45, 12, -1, -3, -2, 0])
    __test(merge_sort, [2, 7, 65, 8, 12, -13, -8, -9, 0])
    __test(inversions_naive, [3, 5, 12, 9, -2, 4, 15])
    __test(inversions_div, [3, 5, 12, 9, -2, 4, 15])
    __test(maxsubarray_naive, [6, 9, 0, 2, 5, 10, 15, 2, 18])
    __test(maxsubarray_div, [6, 9, 0, 2, 5, 10, 15, 2, 18])
    print(product(['A', 'B', 'C', 'D', 'E'], [1, 2, 3]))
    print(product([('A', 'B'), 'C', ('D', 'E')], [1, 2, 3]))
    print(product([('A', 'B'), 'C', ('D', 'E')], [(1, 2), 3]))
    print(product2(['A', 'B', 'C', 'D', 'E'], [1, 2, 3]))
    print(product2([('A', 'B'), 'C', ('D', 'E')], [1, 2, 3]))
    print(product2([('A', 'B'), 'C', ('D', 'E')], [(1, 2), 3]))
    print(summation(['A', 'B', 'C', 'D', 'E'], [1, 2, 3]))
    print(summation([('A', 'B'), 'C', ('D', 'E')], [1, 2, 3]))
    print(summation([('A', 'B'), 'C', ('D', 'E')], [(1, 2), 3]))
    print(summation2(['A', 'B', 'C', 'D', 'E'], [1, 2, 3]))
    print(summation2([('A', 'B'), 'C', ('D', 'E')], [1, 2, 3]))
    print(summation2([('A', 'B'), 'C', ('D', 'E')], [(1, 2), 3]))
    print(summation2(['A', 'B', 'C', 'D', 'E'], [1, 2, 3], False))
    print(summation2([('A', 'B'), 'C', ('D', 'E')], [1, 2, 3], False))
    print(summation2([('A', 'B'), 'C', ('D', 'E')], [(1, 2), 3], False))
    for i in range(6):
        print(shift([1, 2, 3, 4, 5, 6], True, i))
        print(shift([1, 2, 3, 4, 5, 6], False, i))
        print(rotate([1, 2, 3, 4, 5, 6], True, i))
        print(rotate([1, 2, 3, 4, 5, 6], False, i))

    arr = [1, 2, 3, 4, 5, 6]
    print(rotate(arr, True, 3), arr)
    print(n_combinations(5, 2))
    print(n_combinations(5, 3))
    print(n_permutations(5, 2))
    print(n_permutations(5, 3))
    print([x for x in combination2_gen(['A', 'B', 'C', 'D', 'E'])])

    # Computational speed
    for size in [5, 10, 100, 1000, 5000]:
        __speed(summation2, range(size), sample(range(-size, size), size))
        __speed(zip, range(size), sample(range(-size, size), size))


if __name__ == '__main__':
    main()
