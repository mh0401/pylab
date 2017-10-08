# MIT License
# 
# Copyright (c) 2017 mh0401
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

DOXY=doxygen
DOXY_OUTPUT = doc/html doc/doxyerror.log
DEPENDENCIES = doc/Doxyfile.conf doc/doxy_pyfilter
TESTMODULE = test
LINTMODULES = pyart/__main__.py test/test_array.py test/test_combinatorics.py

docs: $(DEPENDENCIES)
	$(DOXY) doc/Doxyfile.conf

quicktest: $(TESTMODULE)
	python3 -m $<

lint: $(LINTMODULES)
	pylint3 --rcfile=.pylintrc $^

clean: $(DOXY_OUTPUT)
	rm -rf $^
