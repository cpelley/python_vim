#!/usr/bin/env python2.7
"""
The following script is used for writing code comments offline and writing
them in a format suitable for the given version control software and
potentially ticketing system.  Example: svn + trac (edgewall).

Example usage
-------------


vim
===

Utilising this script in vim is done by defining a function and associated
command as follows:

    command! -nargs=1 Comment :call Comment(<f-args>)
    function! Comment(tcom)
        :silent execute ":!" s:path . "/../bin/inline_code_comment.py" \
expand('%') line('.') a:tcom ">>" . expand('%') . ".comment" | redraw!
    endfunction

This writes a comment in a file under the same location as the file open in the
current buffer and with name matching that of the file except with suffix
".comment".


Commandline
===========

inline_code_comment.py --help

"""
# Copyright (c) 2017 Carwyn Pelley
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
import subprocess
import sys


NUM_LINES_CONTEXT = 3


class SVN(object):
    @staticmethod
    def uri(filename):
        command = 'svn info {} --xml | grep -oP "(\<relative-url\>)\K[^<]*"'
        uri = subprocess.check_output(command.format(filename), shell=True)
        return uri.replace('\n', '').replace('^/', '')

    @staticmethod
    def revision(filename):
        # broken pipe issue with svn < v1.7 safe to ignore
        # http://subversion.tigris.org/issues/show_bug.cgi?id=3014
        command = ("svn info {} --xml | grep -oP -m 1 "
                   """'.*revision="\K[0-9]*'""")
        return int(subprocess.check_output(command.format(filename),
                                           shell=True))


class Trac(object):
    def __init__(self, version_control):
        self.vc = version_control

    def repo_link(self, filename, lineno):
        return 'source:{}@{}#L{}'.format(self.vc.uri(filename),
                                         self.vc.revision(filename), lineno)

    def code_block(self, filename, lineno):
        with open(filename, 'r') as fh:
            lines = fh.readlines()

        ret = '{{{#!py\n'
        str_format = '{}{} {}'
        for ind, line in enumerate(lines):
            lineno_read = ind + 1
            if ((lineno - NUM_LINES_CONTEXT) <= lineno_read <=
                    (lineno + NUM_LINES_CONTEXT)):
                inline = ' '
                if lineno_read == lineno:
                    inline = '*'
                ret += str_format.format(inline, str(lineno_read), line)
        ret += '}}}'
        return ret

    def __call__(self, filename, lineno, comment=None):
        print self.repo_link(filename, lineno)
        print self.code_block(filename, lineno)
        print comment, '\n'
        print '----', '\n'


def main(fnme, lineno, comment):
    ticketing_handler = Trac(SVN)
    ticketing_handler(fnme, lineno, comment)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        fnme = sys.argv[1]
        lineno = int(sys.argv[2])
        comment = None
        if len(sys.argv) > 3:
            comment = sys.argv[3]
    else:
        sys.exit[0]

    main(fnme, lineno, comment)
