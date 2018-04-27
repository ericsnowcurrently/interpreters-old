from collections import namedtuple
import contextlib
import sys
import tempfile


PRE_CODE = """\
#pymigrate
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

"""


@contextlib.contextmanager
def stdio_to_devnull():
    with tempfile.TemporaryFile() as devnull:
        sys.stdout, sys.stderr = devnull, devnull
        try:
            yield
        finally:
            sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__


class Spec(namedtuple('Spec', 'name summary code exc')):

    def __new__(cls, name, summary, code, exc=None):
        return super(Spec, cls).__new__(cls, name, summary, code, exc)

    @property
    def test_name(self):
        return 'test_' + self.name.replace(' ', '_')

    def add_test_method(self, testclass):
        spec = self

        def test_method(self):
            with stdio_to_devnull():
                spec.run(self)

        test_method.__name__ = spec.test_name
        # XXX Check for duplicates?
        setattr(testclass, spec.test_name, test_method)

    def run(self, testcase):
        code = PRE_CODE + self.code
        if self.exc is None:
            exec(code)
        else:
            with testcase.assertRaises(self.exc):
                exec(code)
