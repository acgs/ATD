__author__ = 'Victor Szczepanski'

import unittest
import os
import sys
from StringIO import StringIO
# We add the parent directories to the path so we can import dockerInvoke
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(PATH)
from ATD.DockerController import dockerController
from contextlib import contextmanager
from StringIO import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

docker_info = ('\n'
               'FROM debian:wheezy\n'
               '\n'
               'ENV DEBIAN_FRONTEND noninteractive\n'
               '\n'
               'RUN apt-get update && apt-get -y upgrade && apt-get clean\n'
               'RUN apt-get -y install --no-install-recommends bash sudo cron vim git python2.7 python-pip sqlite3 ca-certificates  python-sqlite && apt-get clean\n'
               '\n'
               'RUN useradd -m teleceptor\n'
               'USER teleceptor\n'
               'WORKDIR /home/teleceptor/\n'
               'RUN echo  20411 &&  git clone https://github.com/visgence/teleceptor.git\n'
               '\n'
               'WORKDIR /home/teleceptor/teleceptor/unittests/\n'
               '\n'
               '#email_address = test@test.com\n'
               )


class DockerControllerTest(unittest.TestCase):
    """
    DockerControllerTest

    Defines the unit tests for the DockerController module.
    Testing focuses on the run_df function.
    """

    def setUp(self):
        # create fake docker file to use for testing
        with open('./Dockerfile', 'w') as df:
            df.write(docker_info)

    def test_no_dockerfile(self):
        """
        Asserts that dockerController does not raise an exception, but does output a message to stderr.
        :return:
        """
        with captured_output() as (out, err):
            dockerController.run_df()

        self.assertTrue("dockerfilepath cannot be None." in err.getvalue())

    def test_no_email(self):
        """
        Asserts that run_df will successfully run the dockerfile, even without an email address
        :return:
        """

        with captured_output() as (out, err):
            dockerController.run_df("./Dockerfile")

        self.assertIn("Done with dockerfile ./Dockerfile", out.getvalue())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DockerControllerTest, 'test'))  # Using 'test' will use all test functions in TestCase.
    return suite



if __name__ == "__main__":
    unittest.main()