"""
Contributing Authors:
    Mona Assarandarban
    Amirreza Barin
    Jessica Greenling
    Nicholas Nelson

    Reads from dfgen.cfg and produces a Dockerfile based on the info from the config file

Dependencies:
    ConfigParser
    random
    os
    sys
"""

from ConfigParser import SafeConfigParser
import random
import os
import sys
# We add the parent directories to the path so we can import dockerInvoke
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(PATH)

class DFGen(object):

    def __init__(self):
        """
        Gets all of the parameters from dfgen.cfg and sorts them into two lists: required parameters and additional parameters

        :raises ValueError to indicate that a required parameter is messing
        """
        self.configList = SafeConfigParser()

        #check for config file in present directory
        filename = self.configList.read('./dfgen.cfg')
        if len(self.configList.sections()) == 0:
            raise ValueError("Could not find config file containing necessary parameters to generate Dockerfile.")

        #these attributes must be included in dfgen.cfg
        #otherwise, send error message
        requiredList = ['distro', 'apt_dependencies', 'repository_url', 'unit_test_path', 'email_address']
        optionalList = ['pip_dependencies', 'additional_commands', 'test_commands', 'branch_name']
        self.dfList = {}

        for param in requiredList:
            try:
                self.dfList[param] = self.configList.get('Required', param)
            except:
                raise ValueError("Config file missing required parameter %s.", param)

        #TODO: add parameters that aren't required
        for param in optionalList:
            try:
                self.dfList[param] = self.configList.get('Optional', param)
            except:
                self.dfList[param] = None


    def makeDockerfile(self):
        """
        Writes the Dockerfile to file.
        Returns any information useful for rest of ATD, like email.
        :return: A tuple that contains the email address to send failed notifications to, the repository url, and the branch name to pull from the repository..
        """
        with open("./Dockerfile", "w") as file:
            file.write("FROM " + self.dfList['distro'] + "\n\n")
            file.write("ENV DEBIAN_FRONTEND noninteractive" + "\n\n")
            file.write("RUN apt-get update && apt-get -y upgrade && apt-get clean" + "\n")
            file.write("RUN apt-get -y install --no-install-recommends " + self.dfList['apt_dependencies'] + " && apt-get clean" + "\n\n")
            if self.dfList['pip_dependencies'] is not None:
                file.write("RUN pip install " + self.dfList['pip_dependencies'] + "\n\n")
            file.write("RUN useradd -m teleceptor" + "\n")
            file.write("USER teleceptor" + "\n")
            file.write("WORKDIR /home/teleceptor/" + "\n")
            file.write("RUN echo  " + str(random.randint(0,50000)) + " && ")
            file.write(" git clone " + self.dfList['repository_url'])
            if self.dfList['branch_name'] is not None:
                file.write(" && cd teleceptor && git checkout " + self.dfList['branch_name'] + " && cd .. ")
            file.write("\n\n")
            if self.dfList['additional_commands'] is not None:
                file.write("RUN ")
                additionalcmds = ' && '.join(self.dfList['additional_commands'].split(','))
                file.write(additionalcmds + "\n\n")
            file.write("WORKDIR /home/teleceptor" + self.dfList['unit_test_path'] + "\n\n")
            if self.dfList['test_commands'] is not None:
                file.write("RUN echo  " + str(random.randint(0,50000)) + " && ")
                testcmds = ' && '.join(self.dfList['test_commands'].split(','))
                file.write(testcmds + "\n\n")
            file.write("#email_address = " + self.dfList['email_address'] + "\n\n")
        return self.dfList['email_address'], self.dfList['repository_url'], self.dfList['branch_name']


def main(args):
    """
    Makes the Dockerfile
    """
    dfgen = DFGen()
    dfgen.makeDockerfile()


if __name__ == "__main__":
    main(None)
