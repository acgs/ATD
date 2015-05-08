__author__ = 'Victor Szczepanski'
"""
dockerInvokeUnitTests.py


Contributing Authors:
    Mona Assarandarban
    Amirreza Barin
    Jessica Greenling
    Nicholas Nelson
    Victor Szczepanski


Defines the unit tests for dockerInvoke and the DockerInvoker class.


Dependencies:
    unittest
"""

import unittest
import random
import string
import os
import sys
# We add the parent directories to the path so we can import dockerInvoke
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(PATH)
from ATD.DockerInvoke import dockerInvoke


class DockerInvokerTest(unittest.TestCase):
    """
    DockerInvokerTest

    Defines the unit tests for the DockerInvoker class.
    """
    def setUp(self):
        self.invoker = dockerInvoke.DockerInvoker()
        self.randomFileLength = 15  # just an arbitrary choice

    def test_invokeWithDefaultParam_should_fail(self):
        """Checks that invoke with default None parameter raises an OSError exception. """
        self.assertRaises(OSError, self.invoker.invoke)

    def test_invokeWithNoneParam_should_fail(self):
        """Checks that invoke with None parameter raises an OSError exception. """
        self.assertRaises(OSError, self.invoker.invoke, None)

    def test_invokeWithNonExistentFile_should_fail(self):
        """Checks that invoke with a nonexistent file raises an IOError exception.
            Specifically, tests for a file in the current directory with a garbage filename."""
        self.assertRaises(IOError, self.invoker.invoke, './' +
                          ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.randomFileLength)))

    def test_invokeWithGarbageFile_should_fail(self):
        """Checks that invoke with a garbage file path raises an IOError exception.
            This test is distinct from test_invokeWithNonExistentFile_should_fail in that the entire path is garbage."""
        self.assertRaises(IOError, self.invoker.invoke,
                          ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.randomFileLength)))


class DockerInvokeTest(unittest.TestCase):
    """
    DockerInvokeTest

    Defines the unit tests for the DockerInvoke CLI (Command Line Interface)
    """

    def test_NoArg_should_fail(self):
        """
        Checks that CLI will fail when no argument is passed to it for the dockerfile path.
        """
        self.assertRaises(TypeError, dockerInvoke.main)

    def test_NoneArg_should_fail(self):
        """
        Checks that CLI will fail when None is passed as the dockerfile path.
        :return:
        """
        args = dummy()
        args.dockerfile = None
        self.assertRaises(OSError, dockerInvoke.main, args)

class dummy(object):
    """
    The class just serves as a dummy for holding attributes for testing the main function of dockerInvoke.
    """
    def __init__(self):
        self.dockerfile = None

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DockerInvokerTest, 'test'))  # Using 'test' will use all test functions in TestCase.
    suite.addTest(unittest.makeSuite(DockerInvokeTest, 'test'))
    return suite



if __name__ == "__main__":

    unittest.main()