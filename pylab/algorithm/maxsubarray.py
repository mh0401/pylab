"""@package maxsubarray
@brief      Algorithms for determining the subarray with highest total sum.
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@par Details
Max subarray is defined as the subarray with the highest sum in an array.

@parblock
@b Classes
@li N/A

@b Functions
@li maxsubarray_naive    Find the max subarray using brute force.
@li maxsubarray_linear   Find the max subarray in linear time.
@li maxsubarray_div      Find the max subarray using div-conquer.
@li maxsubarray_div2     Find the max subarray using div-conquer (v2).

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
##
def __dc2_find_max_crossing(array, ibegin, imid, iend):
    """Get the maximum sum from the left by adding elements to the left.
    Similarly, get the maximum sum from the right.
    Add them together to get the crossing sum.

    @n @b Performance: @f$ O(n) @f$ @n

    @param array    Array to be searched
    @param ibegin   Left most index to be searched
    @param imid     Midpoint
    @param iend     Right most index to be searched
    @return         Tuple containing the start, end, and sum of the crossing.
    """
    # left side max sum
    runningSum = 0
    leftIdx = 0
    leftSum = -inf
    for k in reversed(range(ibegin, imid + 1)):
        runningSum += array[k]
        if runningSum > leftSum:
            leftSum = runningSum
            leftIdx = k

    # right side max sum
    runningSum = 0
    rightIdx = 0
    rightSum = -inf
    for k in range(imid + 1, iend + 1):
        runningSum += array[k]
        if runningSum > rightSum:
            rightSum = runningSum
            rightIdx = k

    # crossing sum
    return (leftIdx, rightIdx, leftSum + rightSum)


def __dc2_find_max_subarray(array, ibegin, iend):
    """Another algorithm for finding max subarray.
    Main wrapper function to get the maximum subarray.
    Get the subarray out of all possible subarrays of A in which
    the sum of all its elements reflect the highest possible sum.

    @param array    Array to be searched
    @param ibegin   Left most index that will be searched.
    @param iend     Right most index that will be searched.
    @return         Tuple containing the start, end, and sum of the subarray.
    """
    if ibegin == iend:
        return (ibegin, iend, array[ibegin])
    else:
        imid = (ibegin + iend) // 2
        (llx, lrx, lsum) = __dc2_find_max_subarray(array, ibegin, imid)
        (rlx, rrx, rsum) = __dc2_find_max_subarray(array, imid + 1, iend)
        (clx, crx, csum) = __dc2_find_max_crossing(array, ibegin, imid, iend)

        if (lsum >= rsum) and (lsum >= csum):
            return (llx, lrx, lsum)
        elif (rsum >= lsum) and (rsum >= csum):
            return (rlx, rrx, rsum)
        else:
            return (clx, crx, csum)


def __dc_find_msa_linear(array, ibegin, iend):
    """Get the maximum sum out of an array in linear time.
    @n @b Performance: @f$ O(n) @f$ @n

    @param array    Input array
    @param ibegin   Start index of input array
    @param iend     End index of input array

    @return         Tuple containing the start, end, and sum of the subarray.
    """
    # Initialize vars
    runningSum = array[ibegin]
    runningStartIdx = ibegin
    msaSum = array[ibegin]
    msaStartIdx = ibegin
    msaEndIdx = ibegin

    # Determine max sum from the combo
    for k in range(ibegin + 1, iend + 1):
        #print ('Debug: MSA {}, Running {}'.format(msaSum, runningSum))
        runningSum += array[k]
        if array[k] > runningSum:
            runningSum = array[k]
            runningStartIdx = k

        if runningSum > msaSum:
            msaSum = runningSum if runningSum > array[k] else array[k]
            msaStartIdx = runningStartIdx
            msaEndIdx = k
            if runningSum < array[k]:
                runningSum = array[k]

    # Print debug message
    #msg = 'Debug: Array[{}:{}] = {}, MSA({}, {}, {})'
    #print(msg.format(ibegin, iend, array[ibegin:iend+1],
    #                 msaStartIdx, msaEndIdx, msaSum))

    # Return the tuple
    return (msaStartIdx, msaEndIdx, msaSum)


def __dc_find_max_subarray(array, ibegin, iend):
    """Main algorithm entry point.
    Split the array into two equal sizes recursively.
    Determine the max subarray after each split.

    @param array    Array to be sorted
    @param ibegin   The start index of the array to be sorted
    @param iend     The end index of the array to be sorted
    @return         Tuple containing the start, end, and sum of the subarray.
    """
    if ibegin < iend:
        imid = (ibegin + iend) // 2
        msaLeft = __dc_find_max_subarray(array, ibegin, imid)
        msaRight = __dc_find_max_subarray(array, imid + 1, iend)
        msaCombo = __dc_find_msa_linear(array, ibegin, iend)

        # Compare all 3 subarrays and determine the highest.
        # The highest should be the one that is returned.
        if msaCombo[2] >= msaLeft[2] and msaCombo[2] >= msaRight[2]:
            return msaCombo
        elif msaLeft[2] >= msaRight[2] and msaLeft[2] >= msaCombo[2]:
            return msaLeft
        else:
            return msaRight

    # Return original array
    return (ibegin, iend, array[ibegin])


#######################################################
## @publicsection
## @internal
## pylint: disable=W1401
## @endinternal

def maxsubarray_naive(array):
    """Loop through every possible case to get the max subarray.
    @n @b Performance:
    @f$ O(n^2) @f$
    @n

    @param   array  Input array
    @return         Tuple containing the start, end, and sum of the subarray.
    """
    size = len(array)
    if size <= 1:
        return (0, 0, array[0])

    msaSum = array[0]
    msaStartIdx = 0
    msaEndIdx = 0
    for i in range(size):
        runningSum = 0
        for j in range(i, size):
            runningSum += array[j]
            if runningSum > msaSum:
                msaSum = runningSum
                msaEndIdx = j
                if msaStartIdx != i:
                    msaStartIdx = i

    # Return tuple
    return (msaStartIdx, msaEndIdx, msaSum)


def maxsubarray_linear(array):
    """Find the max subarray in linear time.
    NOTE: This is still under debug.

    @n @b Performance:
    @f$ O(n) @f$
    @n

    @param array    Input array
    @return         Tuple containing the start, end, and sum of the subarray.
    """
    return __dc_find_msa_linear(array, 0, len(array) - 1)


def maxsubarray_div(array):
    """Split array into two array of sizes n / 2 recursively.
    Determine the max subarray for each split and combine the result.

    @n @b Performance:
    @f$ T(n) = O(n \hspace{1 mm} {\log_{2} n}) = 2 \hspace{1 mm}
    T(n/2) + O(n) @f$
    @n

    @param array    Array to be searched
    @return         Tuple containing the start, end, and sum of the max subarray.
    """
    return __dc_find_max_subarray(array, 0, len(array) - 1)


def maxsubarray_div2(array):
    """ Different implementation of the algorithm for
    finding max subarray, but still uses divide and conquer approach.
    Split array into two array of sizes n / 2 recursively.
    Determine the max subarray for left, mid, and right splits.
    Compare to get the highest subarray.

    @n @b Performance:
    @f$ T(n) = O(n \hspace{1 mm} {\log_{2} n}) = 2 \hspace{1 mm}
    T(n/2) + O(n) @f$
    @n

    @param array    Array to be searched
    @return         Tuple containing the start, end, and sum of the max subarray.
    """
    return __dc2_find_max_subarray(array, 0, len(array) - 1)
## pylint: enable=W1401
