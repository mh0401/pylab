"""@package sequtils
@brief      Utility functions related to sequences, arrays, lists.
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@par Details
Manipulation of arrays, sequences, lists within itself.

@parblock
@b Classes
@li N/A

@b Functions
@li flatten          Reduce the dimension of an array by 1.
@li product2         Multiply two sequences together.
@li summation2       Sum/join two sequences together.
@li shift            Shift a sequence to the left or right.
@li rotate           Rotate a sequence to the left or right.

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
from . import is_iterable

def flatten(*sequences):
    """Reduce the dimension of an array by 1,
    i.e. it combines list of sequences into a single sequence.
    It assumes that string is not a sequence.
    e.g. [[A, B, C], [D, E]] = ABCDEFGH

    Performance: O(n), n = length of sequence

    @param  sequences   List of sequences.
    @return             All the sequences joined together.
    """
    result = []
    for sequence in sequences:
        if is_iterable(sequence):
            result.extend(sequence)
        else:
            result.append(sequence)
    return tuple(result)


def product2(sequence1, sequence2):
    """Returns the product of two sequences.
    e.g. AB * CD = AC, AD, BC, BD

    Performance: $O(m n)$, m = length of sequence1, n = length of sequence2

    @param  sequence1  List of elements 1
    @param  sequence2  List of elements 2
    @return            Product of both sequences.
    """
    result = []
    for ex1 in sequence1:
        for ex2 in sequence2:
            result.append(flatten(ex1, ex2))
    return result


def product(*sequences):
    """Returns the product of n-sequences.
    Performance: $O(k n^2)$, k = number of sequences to multiply
    """
    result = sequences[0]
    for seq in sequences[1:]:
        result = product2(result, seq)
    return result


def summation2(sequence1, sequence2, alignRight=True):
    """Sum of two sequences. Only sum according to the sequence
    with the lower cardinality.
    This is similar to zip, except zip returns an iterator.

    Performance: O(n), n = length of sequence

    @param   sequence1   The first list of elements
    @param   sequence2   The second list of elements
    @param   alignRight  The sum is aligned to rightmost in sequence (default: True).
    @return              New list which is the sum of both sequences.
    """
    result = []
    size1 = len(sequence1)
    size2 = len(sequence2)
    minsize = size1 if size1 < size2 else size2

    # Determine offset for each sequence addressing
    offset1 = 0
    offset2 = 0
    if alignRight:
        offset1 = 0 if size1 < size2 else abs(size1 - size2)
        offset2 = abs(size1 - size2) if size1 < size2 else 0

    # Join the two sequences
    for idx in range(minsize):
        result.append((sequence1[idx + offset1], sequence2[idx + offset2]))
    return result


def summation(*sequences):
    """Sum of sequences (align to left).
    Only sum according to the sequence with the lowest cardinality.
    This is similar to zip, except zip returns an iterator.

    Performance: O(n*m), n = lowest cardinality, m = number of sequences

    @param   sequences   List of sequences to join.
    @return              New list which is the sum of all sequences.
    """
    result = []
    minsize = min([len(sequence) for sequence in sequences])

    for idx in range(minsize):
        result.append([seq[idx] for seq in sequences])

    return result


def shift(sequence, toRight=True, num=1):
    """Shift a sequence to the right.
    Bounds checking and type checking may return assertion error.

    Performance: O(n), n = number of times to shift

    @param   sequence   Sequence in question.
    @param   toRight    Shift direction is to the right (default: True).
    @param   num        Number of times to shift (default: 1).
    @return             Tuple of the overwritten elements and shifted sequence.
    @throw   AssertionError
    """
    assert num >= 0 and num < len(sequence)
    assert is_iterable(sequence)

    size = len(sequence)
    overwritten = []
    for idx in range(num):
        # Store the element that will be overwritten by shifting.
        overwritten.append(sequence[size - 1 if toRight else 0])

        # Shift
        if toRight:
            sequence[idx + 1:] = sequence[idx:-1]
        else:
            sequence[:-1 - idx] = sequence[1:size - idx]

        #print('Shift: {}, Seq: {}'.format(idx + 1, sequence))

    # Return the leftover
    return overwritten, sequence


def rotate(sequence, toRight=True, num=1, startIdx=0, endIdx=None):
    """Rotation of a sequence. Bounds checking may return an assertion error.

    Performance: O(n), n = number of times to rotate.

    @param   sequence   List of elements.
    @param   toRight    Direction of rotation is to the right (default: True)
    @param   num        Number of times to rotate (default: 1)
    @param   startIdx   Rotate only from this index (default: 0)
    @param   endIdx     Rotate up to this index (default: end)
    @return             Rotated sequence
    @throw   AssertionError
    """
    # default values
    if startIdx is None:
        startIdx = 0
    if endIdx is None:
        endIdx = len(sequence) - 1

    # bounds checking
    assert startIdx >= 0 and startIdx < endIdx and endIdx < len(sequence)
    assert num >= 0
    num = abs(num) % len(sequence)

    # To rotate means to shift and rewrite.
    # Shift first for 'X' amount of times.
    overwritten, sequence = shift(sequence[startIdx:endIdx + 1], toRight, num)

    #print('Rotate: Seq1: {}'.format(sequence))

    # complete rotation by rewriting.
    for idx in range(num):
        sequence[idx if toRight else -1 - idx] = overwritten.pop()

    return sequence
