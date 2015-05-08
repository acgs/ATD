#!/usr/bin/python
"""
Contributing Authors:
    Mona Assarandarban
    Amirreza Barin
    Jessica Greenling
    Nicholas Nelson
    Victor Szczepanski


    DockerInvoke provides the dockerInvoker class to create a docker container
    using a provided dockerfile.

    If this module is run independently, it will attempt to build using a dockerfile in the same directory.


Example Usage:
    python dockerInvoke.py path/to/dockerfile

    or

    ./dockerInvoke.py path/to/dockerfile

Dependencies:
    subprocess
    argparse

"""

import subprocess
import argparse


class DockerInvoker(object):
    """
    Encapsulates docker container creation.
    """

    def __init__(self):
        """
        :return:
        """
        pass

    def invoke(self, dockerfilepath=None):
        """
        Takes a path to a docker file and creates a Docker container for it.
        :param dockerfilepath: The file path as a string. May be relative or absolute.
        :raises OSError: if dockerfilepath does not exist or is None
        :return: The ID of the created container.
        """

        if dockerfilepath is None:
            raise OSError("dockerfilepath cannot be None.")

        try:
            with open(dockerfilepath) as f:
                pass
        except OSError:
            raise OSError("dockerfilepath %s does not exist." % str(dockerfilepath))

        # Redirect stderr to stdout so we can read both in one loop
        df = subprocess.Popen("docker build " + dockerfilepath[:dockerfilepath.rindex('/')+1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        return df


def main(args):
    """
    Makes a DockerInvoker and tries to run invoke using the args.dockerfile.
    :param args: arguments that should contain a dockerfile key or property
    :return:
    """
    cmd_invoker = DockerInvoker()
    cmd_invoker.invoke(args.dockerfile)


def parse_args():
    """
    Parses the arguments from the command line. Expects one argument for the path to the dockerfile.
    :return: the arguments parsed from the command line using argparse.
    """
    parser = argparse.ArgumentParser(description="Creates a new (or returns an equivalent) docker container from a given Dockerfile.")
    parser.add_argument("dockerfile", metavar="D", help="Path to a Dockerfile. May be relative or absolute")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)
