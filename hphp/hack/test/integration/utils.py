from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
import subprocess
import sys

def touch(fn):
    with open(fn, 'a'):
        os.utime(fn, None)

def write_files(files, dir_path):
    """
    Write a bunch of files into the directory at dir_path.

    files: dict of file name => file contents
    """
    for fn, content in files.items():
        path = os.path.join(dir_path, fn)
        with open(path, 'w') as f:
            f.write(content)

def proc_call(args):
    """
    Invoke a subprocess, return stdout, send stderr to our stderr (for
    debugging)
    """
    proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (stdout_data, stderr_data) = proc.communicate()
    print(stderr_data, file=sys.stderr)
    return stdout_data.decode()

def relativize_error_paths(errs):
    """
    Converts the absolute path in "/foo/bar/baz.php:1:1: Error message ..." to
    a relative path

    errs: list of strings
    """
    def relativizer(matchobj):
        return matchobj.group(1) + os.path.basename(matchobj.group(2))

    return [
        re.sub(r'(^ *)([^:]*)', relativizer, line)
        for line in errs
        ]
