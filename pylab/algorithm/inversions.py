"""@package inversions
@brief      Algorithms for counting the number of inversions for Python3.
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@par Details
Inversion is defined as the occurence where an element's value is larger than
that of all the elements that follows.

@parblock
@b Classes
@li N/A

@b Functions
@li inversions_div     Count inversions in an array using divide and conquer.
@li inversions_naive   Count inversions in an array using brute force.

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

#######################################################
## @privatesection

def __dc_count_inversions(array, ibegin, imid, iend):
    """Split array(0..n) into left(0..n/2 + 1) and right(0..n/2).
    Foreach array[p..r], compare left[i] and right[j],
    sort and count inversions.

    @n Performance: @f$ O(n) @f$

    @param  array    Input array
    @param  ibegin   Start index of input array
    @param  imid     Mid index of input array
    @param  iend     End index of input array
    @retval inv      Number of inversions
    """
    # Prepare left and right array.
    # Add sentinel value.
    left = array[ibegin : imid + 1]
    right = array[imid + 1 : iend + 1]
    left.append(inf)
    right.append(inf)
    leftsize = imid - ibegin + 1
    i = 0
    j = 0
    inv = 0

    # Sort the array, at the same time, count the inversion.
    for k in range(ibegin, iend + 1):
        if left[i] <= right[j]:
            array[k] = left[i]
            i += 1
        else:
            # Since sorted, the numbers following
            # this element in the left array must
            # be inversions as well. Add all of them.
            inv += (leftsize - i)
            array[k] = right[j]
            j += 1
    return inv


def __dc_get_inversions(array, ibegin, iend):
    """Main algorithm entry point.
    Split the array into two equal sizes recursively.
    Count and total the result.

    @param  array    Array to be sorted
    @param  ibegin   The start index of the array to be sorted
    @param  iend     The end index of the array to be sorted
    @retval inv      Number of inversions in the array
    """
    inv = 0
    if ibegin < iend:
        imid = (ibegin + iend) // 2
        inv += __dc_get_inversions(array, ibegin, imid)
        inv += __dc_get_inversions(array, imid + 1, iend)
        inv += __dc_count_inversions(array, ibegin, imid, iend)
    return inv


#######################################################
## @publicsection

#pylint: disable=anomalous-backslash-in-string
def inversions_naive(array):
    """Count inversions in an array. Loop through every element
    and determine inversions. Add up all the inversions.

    @n Performance: @f$ \Omega(n) , \hspace{1 mm} O(n^2) @f$

    @param array    Input array
    @retval inv     Number of inversions in the input array.
    """
    size = len(array)
    if size <= 1:
        return 0

    inv = 0
    for i in range(size - 1):
        for j in range(i + 1, size):
            if array[i] > array[j]:
                inv += 1
    return inv


def inversions_div(array):
    """Count inversions using divide and conquer approach.
    Split array into two array of sizes (n / 2) recursively.
    Count the inversion, sum, and report.

    @n @b Performance:
    @f$ T(n) = O(n \hspace{1 mm} {\log_{2} n}) = 2 \hspace{1 mm}
    T(n/2) + O(n) @f$
    @n

    @param array    Array to be searched
    @return         Number of inversions in the array
    """
    return __dc_get_inversions(array, 0, len(array) - 1)

#pylint: enable=anomalous-backslash-in-string
