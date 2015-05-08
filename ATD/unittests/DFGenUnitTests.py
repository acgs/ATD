__author__ = 'Victor Szczepanski'

import unittest
import os
import sys
# We add the parent directories to the path so we can import dockerInvoke
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(PATH)

from ATD.DFGen import dfgen

config_required = (
     "[Required]"
     "\n"
     "distro = debian:wheezy"
     "\n"
     "apt_dependencies = bash sudo cron vim git python2.7 python-pip sqlite3 ca-certificates  python-sqlite"
     "\n"
     "repository_url = https://github.com/visgence/teleceptor.git"
     "\n"
     "unit_test_path = /teleceptor/unittests/"
     "\n"
     "email_address = test@test.com"
     "\n"
    )

config_optional = (
    "[Optional]"
     "\n"
     "test_commands = python functionalTest.py, python stressTest.py, python FailTest.py"
     "\n"
     "pip_dependencies = sqlalchemy cherrypy requests whisper pySerial jinja2"
     "\n"
     "branch_name = master"
     "\n"
    )

config_info = \
    config_required + config_optional

class dfgenTest(unittest.TestCase):

    def setUp(self):
        """
        Creates a dfgen config file with some default values.
        :return:
        """

        #create fake config file to use for testing
        with open('./dfgen.cfg','w') as dfgen_config:
            dfgen_config.write(config_info)

    def takeDown(self):
        """
        Deletes the test dfgen config file.
        :return:
        """
        os.remove("./dfgen.cfg")

    def test_no_config_should_raise_exception(self):
        #remove dfgen.cfg
        os.remove("./dfgen.cfg")
        self.assertRaises(ValueError, lambda: dfgen.DFGen())

    def test_empty_config_raise_valueerror(self):
        os.remove("./dfgen.cfg")
        with open('./dfgen.cfg', 'w') as dfgen_config:
            dfgen_config.write('')

        self.assertRaises(ValueError, lambda: dfgen.DFGen())

    def test_missing_required_should_raise_valueerror(self):
        os.remove("./dfgen.cfg")
        with open('./dfgen.cfg', 'w') as dfgen_config:
            for line in config_required.split('\n'):
                if 'email_address =' in line:
                    continue
                dfgen_config.write(line)

        self.assertRaises(ValueError, lambda: dfgen.DFGen())

    def test_only_required_should_pass(self):
        os.remove("./dfgen.cfg")
        with open('./dfgen.cfg', 'w') as dfgen_config:
            dfgen_config.write(config_required)
        dfgen.DFGen()

    def test_required_and_optional_should_pass(self):
        dfgen.DFGen()

    def test_makedf_only_required_should_create_file(self):
        os.remove("./dfgen.cfg")
        with open('./dfgen.cfg', 'w') as dfgen_config:
            dfgen_config.write(config_required)

        dfgenerator = dfgen.DFGen()

        dfgenerator.makeDockerfile()
        self.assertTrue(os.path.exists('./Dockerfile'))

    def test_makedf_only_required_should_contain_required(self):
        """
        Running makeDockerfile when dfgen was initialized with a file containing only required values,
         Dockerfile output should contain lines only related to the required values.
        """
        os.remove("./dfgen.cfg")
        with open('./dfgen.cfg', 'w') as dfgen_config:
            dfgen_config.write(config_required)

        dfgenerator = dfgen.DFGen()

        dfgenerator.makeDockerfile()
        df_lines = []
        with open('./Dockerfile', 'r') as dockerfile:
            df_lines = dockerfile.readlines()

        for line in df_lines:
            self.assertFalse("RUN pip install" in line)

        fromindex = self._find_str_in_list(df_lines, 'FROM')
        envindex = self._find_str_in_list(df_lines, 'ENV DEBIAN_FRONTEND noninteractive')
        aptget_index = self._find_str_in_list(df_lines, 'RUN apt-get update && apt-get -y upgrade && apt-get clean')
        install_index = self._find_str_in_list(df_lines, 'RUN apt-get -y install --no-install-recommends')
        useradd_index = self._find_str_in_list(df_lines, "RUN useradd -m teleceptor")
        user_index = self._find_str_in_list(df_lines, 'USER teleceptor')
        workdir_index = self._find_str_in_list(df_lines, 'WORKDIR /home/teleceptor/')

        self.assertTrue(fromindex < envindex < aptget_index
                        < install_index < useradd_index < user_index
                        < workdir_index)

    def _find_str_in_list(self, lines, string):
        """
        Searches every string in a list for an input string. Asserts that string is in lines.
        :param lines:
        :param string:
        :return: index in lines string was found at.
        """
        i = 0
        for index, line in enumerate(lines):
            self.assertTrue(index < len(lines)-1 or string in line)
            if string in line:
                i = index
                break
        return i

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(dfgenTest, 'test'))  # Using 'test' will use all test functions in TestCase.
    return suite



if __name__ == "__main__":
    unittest.main()


