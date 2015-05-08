__author__ = 'Victor Szczepanski'


class DockerContainer(object):
    """
    Just a data collection for a container's name, id, and the email address to pass along for notifications
    """
    def __init__(self, name=None, containerid=None, email=None):
        self.name = name
        self.containerID = containerid
        self.email = email


