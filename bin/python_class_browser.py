#!/usr/bin/env python2.7
"""
Function-Class-Method browser for python files.

"""
# Copyright (c) 2013 - 2017 Carwyn Pelley
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
import re


def main(fnme):
    with open(fnme, 'r') as fh:
        lines = fh.readlines()

    parsed = []
    for ind, line in enumerate(lines):
        pattern = ['^[\s]*{}\s'.format(ident) for ident in
                   ['cdef', 'cpdef', 'def', 'class']]
        pattern = '|'.join(pattern)
        if re.match(pattern, line):
            print_line = line.replace('\n', '')
            print_line = print_line.replace(':', '')
            print_line = "{}:{}:'{}'".format(fnme, ind + 1, print_line)
            parsed.append(print_line)
            print print_line


if __name__ == '__main__':
    if len(sys.argv) is 2:
        fnme = sys.argv[1]
    else:
        sys.exit[0]

    main(fnme)
