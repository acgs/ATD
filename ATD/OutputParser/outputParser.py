#!/usr/bin/python
__author__ = 'Victor Szczepanski'
"""

"""
import argparse

class OutputParser(object):
    """
    OutputParser provides an interface for parsing output from an OutputManager (in the format of docker output).
    """
    def __init__(self):
        self.passedTests = []
        self.failedTests = []

    def parse(self, output=()):
        """
        Parses a list of strings to generate a tuple of pass or fail Notifications.
        :param output: a list of strings to parse, where each string is considered newline delimited.
        :returns passedtests and failedtests: lists of strings representing the passed and failed tests.
        """
        hyphens = '-'*70 #delineates failed messages

        for index, line in enumerate(output):

            if "FAIL" in line:
                # We use the index_containing_substring method since some extra characters might appear before or after the hyphens.
                indexOfFirstHyphens = index_containing_substring(output[index:], hyphens) + index # we have to add index since function returns index based on provided list.
                indexOfSecondHyphens = index_containing_substring(output[indexOfFirstHyphens+1:], hyphens) + indexOfFirstHyphens+1
                failedMSG = output[index:indexOfSecondHyphens+1]
                if len(failedMSG) <= 0:  # Can happen when, e.g. line is FAILED (failures=1)
                    continue
                #remove any stderr ANSI control characters
                failedMSG = [i[9:] if i.startswith('\x1b[0m\x1b[91m') else i for i in failedMSG]

                self.failedTests.append(failedMSG)

            elif "__main__" in line:
                failed = False
                # function could be pass or fail, but fail message always appears before this line. So, check in fail list
                for fail in self.failedTests:
                    if len(fail) < 1:
                        continue

                    # Format of a failed line is __main__.FailTest.test00_fail: 0.000 ,
                    # where the test (substring between last . before : and rightmost :) is the name of a failed test.
                    # So, we test if the test name is the name of a failed test.
                    colonindex = line.rindex(':')
                    testdotindex = line[:colonindex].rindex('.')
                    if line[testdotindex+1:colonindex] in fail[0]:
                        # function is a failed test, we can exit loop
                        failed = True
                        break

                if not failed:
                    self.passedTests.append(line)
        return self.passedTests, [''.join(lines) for lines in self.failedTests]

def index_containing_substring(the_list, substring):
    """
    Finds the first instance of a string in a list with the provided substring.
    Borrowed from StackOverflow: http://stackoverflow.com/questions/2170900/get-first-list-index-containing-sub-string-in-python
    :param the_list:
    :param substring:
    :return:
    """
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1


def main(output):

    parser = OutputParser()
    passed, failed = parser.parse(output)
    print "Passed tests: "
    for p in passed:
        print p
    print "Failed tests: "
    for f in failed:
        print f
    print "Number of passed tests: %d" % len(passed)
    print "Number of failed tests: %d" % len(failed)



def parse_args():
    """
    Parses the arguments from the command line. Expects one argument for the containerID
    :return: the argument parsed from the command line using argparse.
    """
    parser = argparse.ArgumentParser(description="Parses a unittest style output.")
    parser.add_argument("outputfile", metavar="D", help="Path to a file with unittest style output")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    with open(args.outputfile) as f:
        lines = f.readlines()
        main(lines)