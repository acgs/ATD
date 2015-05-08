__author__ = 'Victor Szczepanski'

import unittest
import os
import sys
# We add the parent directories to the path so we can import dockerInvoke
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(PATH)

from ATD.ContainerManager import containerManager


class StdoutMock(object):
    """
    Mock for stdout. Has a set of strings to output as if they were newline delimited."
    """
    def __init__(self, *strings):
        if len(strings) > 0:
            self.strings = [s for s in strings]
        else:
            self.strings = []

    def readline(self):
        if len(self.strings) == 0:
            return None
        next_string = self.strings[0]
        self.strings = self.strings[1:]
        return next_string


class PopenRefMock(object):
    """
    Mock for a popen_ref to be used by containerManager. Exposes a poll function, which returns the state of the subprocess."
    """
    def __init__(self, *strings):
        if len(strings) > 0:
            self.stdout = StdoutMock(strings)
        else:
            self.stdout = StdoutMock()

    def poll(self):
        """
        Returns the state of the subprocess this popen is bound to.
        :returns None or negative number: None if process is still running, negative number if terminated.
        Since this is a mock class, will always return -1 if not None.
        """
        return None if len(self.stdout.strings) > 0 else -1

class containerManagerTest(unittest.TestCase):
    """
    containerManagerTest

    Defines the unit tests of the containerManager class.
    """
    def setUp(self):
        """
        Just sets up a containerManager with an empty popen_ref.
        Functions that want to test containerManager's handling of stdout output should make a new manager.
        :return:
        """
        self.manager = containerManager.ContainerManager(PopenRefMock())

    def test_no_popenref_shouldfail(self):
        """
        Tests that containerManager raises a ValueError if no popen is given.
        """
        #We must use lambda here because pyunit expects a callable
        self.assertRaises(ValueError, lambda: containerManager.ContainerManager())

    def test_no_output_shouldbecomedone(self):
        """
        Tests that containerManager eventually sets its status to done when it has no output to process.
        """
        while not self.manager.status:
            pass
        self.assertTrue(self.manager.status)

    def test_no_output_should_no_output(self):
        while not self.manager.status:
            pass
        self.assertTrue(len(self.manager.output) == 0)

    def test_one_line_output_should_become_done(self):
        self.manager = containerManager.ContainerManager(PopenRefMock("INFO:2015-04-19 22:20:54,020 Creating Whisper database with uuid 1"))
        while not self.manager.status:
            pass
        self.assertTrue(self.manager.status)

    def test_one_line_output_should_one_output(self):
        """
        Tests that containerManager gets one line of output after processing one line from stdout.
        """
        self.manager = containerManager.ContainerManager(PopenRefMock("INFO:2015-04-19 22:20:54,020 Creating Whisper database with uuid 1"))
        while not self.manager.status:
            pass
        self.assertTrue(len(self.manager.output) == 1)

    def test_one_line_unicode_output_should_become_done(self):
        self.manager = containerManager.ContainerManager(PopenRefMock(u"[91mINFO:2015-04-19 22:20:54,020 Creating Whisper database with uuid 1"))
        while not self.manager.status:
            pass
        self.assertTrue(self.manager.status)

    def test_one_line_unicode_output_should_one_output(self):
        self.manager = containerManager.ContainerManager(PopenRefMock(u"[91mINFO:2015-04-19 22:20:54,020 Creating Whisper database with uuid 1"))
        while not self.manager.status:
            pass
        self.assertTrue(len(self.manager.output) == 1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(containerManagerTest, 'test'))  # Using 'test' will use all test functions in TestCase.
    return suite



if __name__ == "__main__":
    unittest.main()