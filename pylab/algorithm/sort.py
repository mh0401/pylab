"""@package sort
@brief      Sorting algorithm module for Python3.
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@parblock
@b Classes
@li N/A

@b Functions
@li insertion_sort   Sort an array of numbers by insertion.
@li selection_sort   Sort an array of numbers by finding min value.
@li merge_sort       Sort an array of numbers using divide and conquer.

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
from numpy import inf
from . import swap_inarray

#######################################################
## @privatesection
##
def __merge_sort_combine(array, ibegin, imid, iend):
    """Split array(0..n) into left(0..n/2 + 1) and right(0..n/2).
    Foreach array[p..r], compare left[i] and right[j],
    and assign order.

    @n Performance: @f$ O(n) @f$

    @param array    Input array
    @param ibegin   Start index of input array
    @param imid     Mid index of input array
    @param iend     End index of input array

    @retval array   Sorted array
    """
    # Prepare left and right array.
    # Add sentinel value.
    leftArr = array[ibegin : imid + 1]
    rightArr = array[imid + 1 : iend + 1]
    leftArr.append(inf)
    rightArr.append(inf)
    i = 0
    j = 0

    # Assign lowest number between left and right array
    # into the main array for every element in the main array.
    for k in range(ibegin, iend + 1):
        if leftArr[i] <= rightArr[j]:
            array[k] = leftArr[i]
            i += 1
        else:
            array[k] = rightArr[j]
            j += 1
    return array


def __merge_sort_main(array, ibegin, iend):
    """Main algorithm entry point.
    Split the array into two equal sizes recursively.
    Sort and combine/merge from both results.

    @param array    Array to be sorted
    @param ibegin   The start index of the array to be sorted
    @param iend     The end index of the array to be sorted
    @retval array   Sorted array
    """
    if ibegin < iend:
        imid = (ibegin + iend) // 2
        __merge_sort_main(array, ibegin, imid)
        __merge_sort_main(array, imid + 1, iend)
        __merge_sort_combine(array, ibegin, imid, iend)
    return array


#######################################################
## @publicsection
##

#pylint: disable=anomalous-backslash-in-string
def merge_sort(array):
    """Sorts an array of numbers in ascending order, not in-place,
    using divide and conquer approach. Recursively split the array
    into half, reorder, and combine them.

    @n @b Performance:
    @f$ T(n) = O(n \hspace{1 mm} {\log_{2} n}) = 2 \hspace{1 mm} T(n/2) + O(n) @f$
    @n

    @param array    Array to be sorted
    @retval array   Sorted array
    """
    return __merge_sort_main(array, 0, len(array) - 1)
#pylint: enable=anomalous-backslash-in-string


def insertion_sort(array):
    """Sorts an array of numbers in ascending order, in-place.
    For every element, insert the element into the proper index.

    @n @b Performance:
    @f$ O(n^2) @f$
    @n

    @param array    Array to be sorted
    @retval array   Sorted array
    """
    size = len(array)
    if size > 1:
        # For each element in array,
        # insert into its proper index.
        for i in range(1, size):
            insertAtIdx = i

            # Compare elements to detect proper position.
            # Identify index whose element value is lower.
            for j in reversed(range(i)):
                if array[i] < array[j]:
                    insertAtIdx = j

            # Insert the element into proper position.
            if insertAtIdx != i:
                val = array.pop(i)
                array.insert(insertAtIdx, val)

    # Return sorted array.
    return array


def selection_sort(array):
    """Sorts an array of numbers in ascending order, in-place.
    For every position in the array, find the min value of
    the sub-array starting from that position.
    Assign that min value to that position.

    @n @b Performance:
    @f$ O(n^2) @f$
    @n

    @param   array   Array to be sorted
    @retval  array   Sorted array
    """
    size = len(array)
    if size > 1:
        for i in range(size):
            minidx = i

            # Find the index associated with min value
            # of subarray starting at 'i'.
            for j in range(i, size):
                if array[j] < array[minidx]:
                    minidx = j

            # Swap value of index of min value and current index.
            if minidx != i:
                swap_inarray(array, minidx, i)

    # Return sorted array
    return array
