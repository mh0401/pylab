"""@package error
@brief   Exception classes
@author  Marcel H
@date    2017

@parblock
@b Classes
@li N/A

@b Functions
@li N/A

@b Exceptions
@li Error          --- Abstract class for Error exception.
@li TypeCheckError --- Error due to type checking.
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
class Error(Exception):
    """Base class for error"""
    pass


class TypeCheckError(TypeError):
    """Error due to type checking"""

    def __init__(self, typeActual, typeExpected):
        super().__init__()
        self.__actual = typeActual
        self.__expected = typeExpected

    def __str__(self):
        return 'Type mismatch! Expected {} got {}.'.format(
              self.__expected.__qualname__, self.__actual.__qualname__)
