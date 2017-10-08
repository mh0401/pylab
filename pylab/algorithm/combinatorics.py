"""@package combinatorics
@brief      Calculate combination and permutation
@author     Marcel H  @<hmxmail0401@gmail.com@>
@date       2017
@version    0.0

@par Details
Combination and permutation.

@parblock
@b Classes
@li N/A

@b Functions
@li permutations     Returns a list of all permutations of a sequence.
@li combinations     Returns a list of all combinations of a sequence.
@li n_permutations   Returns the number of permutations.
@li n_combinations   Returns the number of combinations.

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
from . import assert_type, is_iterable, product2

## TODO: Implement multi-selection combination.
## TODO: Implement multi-selection permutation.

def __check_input(sequence, select):
    """Checks whether the input sequence and selection is valid.
    Throws an assertion error when sequence is not an iterable.

    @param   sequence        Sequence of elements
    @param   select          Tuple length of combination or permutation.
    @throw   AssertionError
    """
    # Check type first
    assert is_iterable(sequence)
    assert_type(select, int)

    # Check input values after checking the type.
    assert len(sequence) >= select
    assert select > 0


def __combination2_merge(sequence, result):
    """Merge sequences together"""
    # TODO: Fix this/complete the implementation
    hsize = len(sequence) // 2
    for element in sequence[:hsize]:
        result.extend(product2(element, sequence[hsize:]))


def __combination2_div(sequence, result):
    """Generate all combinations of 2 tuple. Uses an algorithm of divide and conquer.
    Main algorithm entry point.

    @param  sequence    Sequence of elements
    @param  result      List of all 2-tuple combinations.
    @throw  AssertionError
    """
    size = len(sequence)
    if size > 1:
        __combination2_div(sequence[:size // 2], result)
        __combination2_div(sequence[size // 2:], result)
        __combination2_merge(sequence, result)


def combination2_div(sequence):
    """Given a sequence, generate all combinations of 2 tuple.
    Uses an algorithm of divide and conquer.

    @param  sequence    Sequence of elements
    @return             List of all 2-tuple combinations.
    @throw  AssertionError
    """
    __check_input(sequence, 2)
    result = []
    __combination2_div(sequence, result)
    return result


def combination2_gen(sequence):
    """Given a sequence, generate all combinations of 2-tuple.
    Returns a generator class.
    Throws an assertion error when sequence is a not a sequence.

    @param  sequence    Sequence of elements
    @return             Generator of all the combinations of 2-tuple.
    @throw  AssertionError
    """
    __check_input(sequence, 2)
    for i, element1 in enumerate(sequence):
        for element2 in sequence[i + 1:]:
            yield element1, element2


def n_permutations(choices, pick):
    """Returns the number of permutations from available choices given selection.
    (order matters, e.g. ABC != BCA)
    @param   choices  The number of available choices.
    @param   pick     The number of selection.
    @return           The number of permutations that can be made.
    """
    total = 1
    for idx in range(pick):
        total *= (choices - idx)
    return total


def n_combinations(choices, pick):
    """Returns the number of combinations from available choices given selection.
    (order does not matter, e.g. ABC == BCA).
    @param   choices  The number of available choices.
    @param   pick     The number of selection.
    @return           The number of permutations that can be made.
    """
    return n_permutations(choices, pick) // n_permutations(pick, pick)
