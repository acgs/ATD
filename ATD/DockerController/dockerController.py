#!/usr/bin/python
__author__ = 'Nicholas Nelson'
"""
Contributing Authors:
    Nicholas Nelson
    Victor Szczepanski
    
    Entry point of ATD.
    Manages the invocations and interaction between: DFGen, DockerInvoker, ContainerManager,
        OutputManager, Parser, and Notifier

Example Usage:
    python dockerController.py

    or

    ./dockerController.py 
"""
import os
import sys
import argparse
import multiprocessing
import threading
import time
import itertools
# We add the parent directories to the path so we can import dockerInvoke and containerManager
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(PATH)
from DockerInvoke.dockerInvoke import DockerInvoker
from ContainerManager.containerManager import ContainerManager
from OutputManager.outputManager import OutputManager
from DFGen.dfgen import DFGen
from Notifier.Notifier import Notify

def run_df(dockerfile=None, email=None):
    """
    Static function to run a dockerfile.

    In particular, this function invokes the dockerfile, thereby creating a docker container and executing the commands in the dockerfile.
    Then, we bind this to a ContainerManager to monitor and gather output from the docker containers. Finally, this is passed on the the output manager.
    :param dockerfile: The path to a dockerfile directory.
    :param email: The email address specified by the user.
    :return : A message showing completion or error with test suite.
    """
    #TODO: run_df should be able to take a list of dockerfiles to run sequentially.
    print "Running dockerfile %s" % str(dockerfile)
    di = DockerInvoker()
    try:
        df = di.invoke(dockerfile)
    except OSError as e:
        sys.stderr.write(e.message)
        return
    cm = ContainerManager(df)
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    t = threading.Thread(target=cm.monitor)
    t.start()
    #TODO: Refactor the following printing setup so that ContainerManager tells us what state it is in (e.g. what step)
    sys.stdout.write('\n\r')
    currentline = ""
    while not cm.status:
        if len(cm.output) > 0 and "Step " in cm.output[-1] and currentline != cm.output[-1][:cm.output[-1].index(':')]:
            sys.stdout.write('\r' ' '*len(currentline) + '\r')
            currentline = cm.output[-1][:-1] # cm.output[-1][:cm.output[-1].index(':')]
        sys.stdout.write("running docker... " + currentline + " " + spinner.next())
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write('\r')
    t.join()
    sys.stdout.write('\r')

    om = OutputManager(cm.output)
    passedTests, failedTests = om.run()

    notifier = Notify()
    notifier.send_notification(email,failedTests, passedTests)

    print "Done with dockerfile %s" % str(dockerfile)

    if 'Successfully built' in cm.output[-2]:
        print "Testing suite completed properly."
    else:
        print "Error with testing suite."


class DockerController(object):
    def __init__(self, *dockerfiles):
        self.dockerfiles = dockerfiles

    def run_dfs(self, email=None):
        """
        Spins off a subprocess for each dockerfile this DockerController is responsible for. Runs the run_df function in each subprocess.
        :param email: email to send any failed notifications to.
        :return:
        """
        #TODO: Decide if we should create a process for each dockerfile, or create as many processes as cores and split self.dockerfiles up among those processes.
        # Current implementation starts a process for each dockerfile.
        for dockerfile in self.dockerfiles:
            p = multiprocessing.Process(target=run_df, args=(dockerfile, email))
            p.start()


def main(args):
    """
    Generates a dockerfile and activates ATD with that dockerfile.
    :param args: Currently unused.
    :return:
    """

    dfgen = DFGen()
    email, url, branchname = dfgen.makeDockerfile()
    controller = DockerController(os.path.abspath('./Dockerfile'))
    controller.run_dfs(email)
    
if __name__ == '__main__':
    main(None)
