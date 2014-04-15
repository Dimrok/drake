# Copyright (C) 2009-2014, Quentin "mefyl" Hocquet
#
# This software is provided "as is" without warranty of any kind,
# either expressed or implied, including but not limited to the
# implied warranties of fitness for a particular purpose.
#
# See the LICENSE file for more information.

import subprocess
import drake
import platform
import string
import random

from .. import Path, Exception

def check_version(expected, effective):

    try:
        iter(expected)
        return effective in expected
    except TypeError:
        return effective == expected


class Value(drake.Node):

    """A Node whose file contain a serialized python value.

    >>> path = '/tmp/.drake.value'
    >>> with open(path, 'w') as f:
    ...   print('42', file = f)
    >>> n = Value(path)
    >>> assert n.value() == 42
    """

    def value(self):
        """The serialized python value."""
        if not self.path().exists():
            raise Exception('%s: python.Value node must be built first.' % self)
        with open(str(self.path()), 'r') as f:
            return eval(f.read())

    def write(self, value):
        with open(str(self.path()), 'w') as f:
            print(repr(value), file = f)


class _PasswordGenerator(drake.Builder):

    def __init__(self, target, length = 8):
        assert isinstance(target, Value)
        self.__target = target
        self.__length = length
        drake.Builder.__init__(self, [], [self.__target])

    def execute(self):
        self.output("password (length: %s) %s" % (self.__length, self.__target),
                    "Password %s" % self.__target)
        pw = ''.join([random.choice(string.ascii_letters
                                    + string.digits
                                    + string.punctuation)
                      for i in range(self.__length)])
        self.__target.write(pw)
        return True


class Password(Value):

    """A Value storing a random password.

    >>> pw = Password('/tmp/.drake.password')
    >>> pw.path().remove()
    >>> pw.build()
    Password /tmp/.drake.password
    >>> assert isinstance(pw.value(), str)
    >>> assert len(pw.value()) == 8

    Generated password can be customized.

    >>> pw = Password('/tmp/.drake.password.custom', length = 12)
    >>> pw.path().remove()
    >>> pw.build()
    Password /tmp/.drake.password.custom
    >>> assert len(pw.value()) == 12

    The password value can also be forced.

    >>> pw = Password('/tmp/.drake.password.forced', value = '_o< COIN')
    >>> pw.value()
    '_o< COIN'
    >>> pw.build()
    >>> pw.value()
    '_o< COIN'
    """

    def __init__(self, name, length = 8, value = None):
        """Construct a Password.

        name   -- the node name.
        length -- the length in characters of the generated password.
        """
        Value.__init__(self, name)
        _PasswordGenerator(self, length = length)
        if value is not None:
            self.write(value)


class Python:

    def __init__(self, major, minor = None, modules = [], prefix = None):

        if prefix is None:
            test = ['/usr', '/usr/local']
        else:
            test = [prefix]


        self.prefix = None
        for path in test:
            p = Path(path)
            if not p.absolute:
                p = drake.Drake.current.path_source / p
            if (p / 'bin/python').exists():
                self.prefix = p
                break

        if self.prefix is None:
            raise Exception('unable to find bin/python in %s' % ', '.join(test))

        self.python = self.prefix / 'bin/python'

        self.major = eval(subprocess.getoutput('%s -c \"import sys\nprint sys.version_info[0]\"' % self.python))
        self.minor = eval(subprocess.getoutput('%s -c \"import sys\nprint sys.version_info[1]\"' % self.python))

        if not check_version(major, self.major):
            raise Exception('invalid python major version: expected %s.x, got %s.%s' % (major, self.major, self.minor))
        if not check_version(minor, self.minor):
            raise Exception('invalid python minor version: expected %s.%s, got %s.%s' % (major, minor, self.major, self.minor))

        linux_command = {
          'Ubuntu': 'apt-get install %s'
          }


        linux_pck = {
          'xml.dom.ext': {
            'Ubuntu': 'python-xml'
            }
          }

        for module in modules:
            if subprocess.getstatusoutput('%s -c \'import %s\'' % (self.python, module))[0] >> 8 != 0:
                msg = 'missing python module %s' % module
                if platform.system() == 'Linux':
                    distro = platform.linux_distribution()[0]
                    if module in linux_pck \
                          and distro in linux_pck[module]:
                        pck = linux_pck[module][distro]
                        cmd = linux_command[distro]
                        msg = '%s - try `%s\'' % (msg,cmd % pck)
                raise Exception(msg)
