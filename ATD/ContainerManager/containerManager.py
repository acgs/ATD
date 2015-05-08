#!/usr/bin/python
__author__ = 'Victor Szczepanski'
"""
Contributing Authors:
    Nicholas Nelson
    Victor Szczepanski


    ContainerManager provides the containerManager class to handle executing tests in a docker container
    and getting the output.

"""

import threading


class ContainerManager(object):
    def __init__(self, popen_ref=None):
        """
        Creates a ContainerManager and starts a thread to monitor the provided reference from Popen.
        :param popen_ref: Reference to the Popen object created for a docker process (e.g. docker build, docker run, etc.)
        :raises RuntimeError: If this ContainerManager fails to create the monitoring thread, this exception is raised.
        """
        if popen_ref is None:
            raise ValueError("No reference to docker process.")

        self.dockerProcess = popen_ref

        self._output = []  # Maps the filename to its output.
        self.thread = None
        self._status = False
        
        try:
            self.__spawnmonitorthread()
        except RuntimeError as e:
            print "Error creating monitoring thread."
            raise e

    def monitor(self):
        """
        Collects the output from the docker process serially.
        Does not spawn any threads.

        Note that we are not using this function and may want to remove it.
        
        :return: The output on stdout from dockerProcess, split by newline.
        """
        return self.__collectoutput()

    def __spawnmonitorthread(self):
        """
        Creates a thread to collect the output from the docker process, and starts the thread.
        :raises: RuntimeError if thread failed to start
        """
        print "Creating monitor thread."
        self.thread = threading.Thread(target=self.__collectoutput)
        self.thread.start()

    def __collectoutput(self):
        """
        Private function to sit and read output on stdout from this ContainerManager's dockerProcess.
        This function blocks on the output from the docker process.
        :return: A list of the output on stdout from dockerProcess, split by newline.
        :raises TypeError: If this containerManager's process reference is invalid.
        """
        if self.dockerProcess is None:
            raise TypeError("This ContainerManager does not have an appropriate dockerProcess reference (value is None)")

        # Recipe to get output line by line and print it as well.
        while self.dockerProcess.poll() is None:
            line = self.dockerProcess.stdout.readline()
            self.output.append(line)

        self._status = True
        return self.output

    @property
    def status(self):
        """
        Wrapper to get state of docker monitoring thread.
        TODO: Make return status more meaningful, perhaps with some constants.
        :return: True if thread is running, False otherwise (including if thread has not been run yet).
        """
        return self._status

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        """
        Setter for output. We do not permit external modification to output, so this just raises an AttributeError.
        :param value: Value to set output to.
        :raises AttributeError: output can not be modified.
        """
        raise AttributeError("output of this class may not be modified externally.")
