#!/usr/bin/env python
"""
Monkeypatch for pyflakes to produce a syntax error consistent with the
formatting of other error types.

"""
# Copyright (c) 2013 Carwyn Pelley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import pyflakes.reporter as reporter
from pyflakes.scripts.pyflakes import main


# Monkey patch syntax error method for suitability with vim
def vimhappy_syntaxError(self, filename, msg, lineno, offset, text):
    line = text.splitlines()[-1]
    if offset is not None:
        offset = offset - (len(text) - len(line))
    self._stderr.write(reporter.u('%s:%d:%d: %s\n') % (filename, lineno,
                       offset + 1, msg))


if __name__ == '__main__':
    reporter.Reporter.syntaxError = vimhappy_syntaxError
    main(sys.argv[1:])
