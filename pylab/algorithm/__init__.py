"""@package algorithm

@brief Algorithm implementation and testing.

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
from ..utils import swap_inarray, assert_type, is_iterable
from .sequtils import flatten, product2, product, summation2, summation, shift, rotate
from .sort import merge_sort, selection_sort, insertion_sort
from .inversions import inversions_div, inversions_naive
from .maxsubarray import maxsubarray_div, maxsubarray_div2, \
                        maxsubarray_linear, maxsubarray_naive
from .combinatorics import n_combinations, n_permutations, \
                            combination2_div, combination2_gen

__all__ = ['product2', 'product', 'flatten', 'summation2', 'summation',
           'shift', 'rotate',
           'merge_sort', 'selection_sort', 'insertion_sort',
           'inversions_div', 'inversions_naive',
           'n_combinations', 'n_permutations',
           'combination2_div', 'combination2_gen',
           'maxsubarray_div', 'maxsubarray_div2',
           'maxsubarray_naive', 'maxsubarray_linear']
