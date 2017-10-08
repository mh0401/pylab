"""@package utils

@brief Utility functions for Python 3.5.x and above.

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
from .error import TypeCheckError
from .tools import Traceable, Verbosity, ListIterator, typename, fullobjname, \
                   str_current_time, join_recursive, swap_inarray, \
                   find_uniques_consecutive, get_uniques, split, getobj, \
                   is_file, is_dir, check_dir, assert_cond, assert_type, \
                   is_iterable

__all__ = ['TypeCheckError', 'Traceable', 'ListIterator', 'Verbosity',
           'str_current_time', 'typename', 'fullobjname', 'swap_inarray',
           'join_recursive', 'find_uniques_consecutive', 'get_uniques', 'split', 'getobj',
           'is_file', 'is_dir', 'check_dir', 'assert_cond', 'assert_type',
           'is_iterable']
