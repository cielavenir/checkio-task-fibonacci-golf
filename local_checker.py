#!/usr/bin/env python

# Print "compiled size".
# They say Ruby can use YARVCore::InstructionSequence, but I cannot find any examples.
# Note: if MAJOR or MINOR version changes, rejudge is required (TEENY does not matter).

# Due to optimize=1 flag, Python 3.2+ is required.

import marshal


def check_code(codestring):
    codestring = codestring.replace("\r\n", "\n")
    codestring = codestring.replace("\r", "\n")
    codestring = codestring.rstrip()
    try:
        return len(marshal.dumps(__builtins__.compile(codestring, '', 'exec', optimize=1)))
    except SyntaxError as detail:
        import traceback

        lines = traceback.format_exception_only(SyntaxError, detail)
        for line in lines:
            print(line.replace('File "<string>"', ''))
        return None


if __name__ == '__main__':
    # cf: http://www.opensource.apple.com/source/python/python-3/python/Lib/py_compile.py
    import sys

    if len(sys.argv) < 2:
        print('local_checker py...')
        sys.exit(1)
    for i in range(1, len(sys.argv)):
        f = open(sys.argv[i])
        codestring = f.read()
        f.close()
        len = check_code(codestring)
        print(len)