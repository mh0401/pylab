"""@package tools
@brief   Utility tool sets
@author  Marcel H
@date    2017

@parblock
@b Classes
@li Traceable           Base class for adding traceability and debuggability.

@b Functions
@li typename                   Retrieve type name of an object.
@li fullobjname                Retrieve full name (incl. module) of an object.
@li str_current_time           Retrieve current time in string format.
@li join_recursive             Join string list or tuples recursively.
@li getobj                     Get an object from a module.
@li is_iterable                Returns true if its an iterable.
@li split                      Split an array according to the indices given.
@li find_uniques_consecutive   Find consecutive duplicates within the array.
@li get_uniques                Get elements that are duplicated within the array.
@li is_file                    Determine whether a string refers to a file.
@li is_dir                     Determine whether a string refers to a directory.
@li resolve                    Resolve directory.
@li check_dir                  Raises an exception if directory is invalid.
@li assert_cond                Assert that a condition is true.
@li assert_type                Type checking w/ assertion.
@li swap_inarray               Swaps 2 elements inside an array.
@li geo_seq                    Geometric sequence

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
from pathlib import Path
from typing import Iterable
from operator import xor
from time import strftime, gmtime, process_time
from importlib import import_module
from enum import IntEnum, unique
from . import TypeCheckError

######################################################
## @publicsection


def typename(obj):
    """Get the qual name of an object.
    @param  obj   Object in question.
    @return       The type of the object.
    """
    return obj.__name__ if hasattr(obj, '__name__') else type(obj).__qualname__


def fullobjname(obj):
    """Get the full name of an object (including its module).
    @param  obj   Object in question.
    @return       Module name <.> object name.
    """
    return obj.__module__ + '.' + typename(obj)


def str_current_time():
    """Returns the current time string format for suffix to a string.
    @return     Current time string format of yy_mm_dd_hr_min_sec_timezone
    """
    return strftime("%Y_%m_%d_%H_%M_%S_%Z", gmtime())


def join_recursive(lst, sep):
    """Utility function for joining string tuples recursively.
    @param  lst  List or tuple to be joined which contain list/tuples within.
    @return      Joined string
    """
    msg = ''
    for i in lst:
        if isinstance(i, tuple) or isinstance(i, list):
            msg += join_recursive(i, sep)
        else:
            msg += (i + sep)
    return msg


def getobj(modulename, objname):
    """Get sorting function associated with the function name.
    @param  modulename  Module name of the given object.
    @param  objname     Name of the desired object.
    @return             Desired object.
    """
    return getattr(import_module(modulename), objname)


def is_iterable(obj, isStrIterable=False):
    """Returns true if an object is iterable.
    @param  obj            Object in question.
    @param  isStrIterable  String is an iterable (default: False).
    """
    if not isinstance(obj, Iterable):
        return False
    else:
        # XNOR is an iff statement A XNOR B = A iff B
        return not xor(isStrIterable, isinstance(obj, str))


def split(array, indexes):
    """Split an array according to the indexes given.
    @param   array    Array to be split
    @param   indexes  Index as integer or list.
    @return           Array split
    """
    if isinstance(indexes, int):
        return list(array[0:indexes], array[indexes:])

    newarray = []
    offset = 0
    for idx in indexes:
        newarray.append(array[offset:idx])
        offset += idx
    if indexes[-1] < len(array):
        newarray.append(array[indexes[-1]:])
    return newarray


def find_uniques_consecutive(array):
    """Find unique elements within the array consecutively.
    @param   array   Array to look into.
    @return          The indices of the unique elements.
    """
    val = array[0]
    indices = []
    for idx, element in enumerate(array):
        if element != val:
            indices.append(idx)
            val = element
    return indices


def get_uniques(array):
    """Get unique elements within an array.
    i.e. All other elements in the array are duplicates of the unique elements.
    @param   array   Array to look into.
    @return          The list of unique elements
    """
    uniques = []
    for element in array:
        if element not in uniques:
            uniques.append(element)
    return uniques


def is_file(argstr):
    """Platform independent method for determining whether a string
    refers to a file.
    @param  argstr  Any string argument
    @return         Returns true if it is a file, false otherwise.
    """
    argf = Path(argstr)
    return argf.exists() and argf.is_file()


def is_dir(argstr):
    """Platform independent method for determining whether a string
    refers to a directory.
    @param  argstr  Any string argument
    @return         Returns true if it is a directory, false otherwise.
    """
    arg = Path(argstr)
    return arg.exists() and arg.is_dir()


def resolve(name):
    """Platform independent method for resolving a directory.
    @param  name    Directory name (absolute/relative)
    @return         String representation of the directory
    """
    arg = Path(name)
    return str(arg.resolve())


def check_dir(dirname):
    """Check if the directory is valid.
    @param  dirname     Directory to be checked
    @throw  FileNotFoundError
    """
    print('Checking directory...{}'.format(dirname))
    if dirname is not None and not is_dir(dirname):
        raise FileNotFoundError('{} is not a valid directory'.format(dirname))


def get_full_filename(dirname, name, ext, tmstamp=False):
    """Returns full file name given all necessary information.
    Checks and resolves directory and formats the get_full_filename.

    @param  dirname  Directory of where the log file should be.
    @param  name     File name
    @param  ext      File extension
    @param  tmstamp  Whether to add timestamp or not.
    @return          Full log file name.
    """
    fill = '_' + str_current_time() if tmstamp else ''
    fmt = '/{}{}{}' if ext.startswith('.') else '/{}{}.{}'
    return resolve(dirname) + fmt.format(name, fill, ext)


def assert_cond(cond, exc):
    """Assert a condition. Raise an error if the condition is not true.
    @param  cond  Condition that the assertion evaluates.
    @throw  exc   Exception that will be thrown when not quiet.
    """
    if not cond:
        raise exc


def assert_type(instance, classtype):
    """Type checking with assertion.
    @param  instance    Any object or instance.
    @param  classtype   Expected or desired type of the object.
    @throw  TypeCheckError
    """
    assert_cond(isinstance(instance, classtype), TypeCheckError(type(instance), classtype))


def swap_inarray(array, idx1, idx2):
    """ Swap two elements in an array.

    @param  array    Input array
    @param  idx1     Index of first element
    @param  idx2     Index of second element
    @retval array    Array after swapping
    """
    if idx1 != idx2:
        temp = array[idx1]
        array[idx1] = array[idx2]
        array[idx2] = temp
    return array


#pylint: disable=anomalous-backslash-in-string
def geo_seq(val, ratio, length):
    """Returns an array of geometric sequence.

    @n @f$ a , \hspace{1 mm} a r , \hspace{1 mm} a r^2 ,
    \hspace{1 mm} \dots \hspace{1 mm}, \hspace{1 mm}
    a_{n-1} \hspace{1 mm} r^{n-1} @f$ @n

    @param val      Start value of the geometric sequence (a)
    @param ratio    Ratio (r)
    @param length   Sequence length (n)

    @return Array of geometric sequence
    """
    return [val * pow(ratio, i) for i in range(length)]
#pylint: enable=anomalous-backslash-in-string


@unique
class Verbosity(IntEnum):
    """Enumeration for verbosity level"""
    ERROR = 0
    WARNING = 1
    NONE = 2
    INFO = 3
    DEBUG = 4


class Traceable(object):
    """Base class with verbosity and debug flag as default attribute."""

    ## Static variables
    verbosity = Verbosity.NONE
    debug = 0
    DEBUG_ENABLE = 0

    def __init__(self):
        super().__init__()

    @classmethod
    def is_debug(cls):
        """Returns whether this object is in debug mode."""
        return Traceable.debug & cls.DEBUG_ENABLE

    @classmethod
    def print_tr(cls, msg, threshold):
        """Print only if the verbosity is above the threshold.
        @param  msg          Message to be printed out.
        @param  threshold    Verbosity threshold level.
        """
        if Traceable.verbosity >= threshold:
            print('{:.6f} sec: [{}] {}'.format(process_time(), cls.__qualname__, msg)) #pylint: disable=no-member


class ListIterator: #pylint: disable=too-few-public-methods
    """Iterator class for a list."""

    def __init__(self, lst):
        """Constructor"""
        self.__idx = 0
        self.__lst = lst
        self.__n = len(lst)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__idx < self.__n:
            self.__idx += 1
            return self.__lst[self.__idx - 1]
        else:
            raise StopIteration()
