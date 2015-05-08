#!/usr/bin/python
__author__ = 'Nicholas Nelson'
"""
Contributing Authors:
    Nicholas Nelson
    Amirreza Barin
    Mona Assarandarban
    
    Parses output from containerManager
"""
import os
import sys
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(PATH)
from Notification.Notification import PassNotification, FailNotification
from OutputParser.outputParser import OutputParser

class OutputManager(object):
    def __init__(self, output=None):
        self._output = output
        self.passNotes = []
        self.failNotes = []

    def run(self, output=None):
        """
        :returns passed, failed: Lists of passed and failed notifications
        """
        if output is None:
            output = self._output
        with open("./logfile.txt" , "w+") as f:
            f.write('\n'.join([str(item) for item in output]))
        op = OutputParser()
        passed, failed = op.parse(output)

        for pn in passed:
            self.passNotes.append(PassNotification(pn))
        for fn in failed:
            self.failNotes.append(FailNotification(fn))
        """
        print "Passed tests: "
        for p in passed:
            print p
        print "Failed tests: "
        for f in failed:
            print f
        print "Number of passed tests: %d" % len(passed)
        print "Number of failed tests: %d" % len(failed)
        """
        return passed, failed

    def do_notify(self):
        pass
    
"""
    InfoList=[]
    ErrorList=[] 
    for word in output:
	if word.startswith('INFO'):
		InfoList.append(word)
	elif word.startswith('ERROR'):
                ErrorList.append(word)

    
    print '\n'.join(InfoList)
    print '\n'.join(ErrorList)
"""
"""
class PassNotification(OutputManager):
    def __init__(self):
        super().__init__(self,InfoList)
        run(self.InfoList)

    def run(self):
    	print '\n'.join(self.InfoList)
        print '\n'.join(InfoList) 
"""
