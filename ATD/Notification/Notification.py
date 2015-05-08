__author__ = 'greenpants'


class Notification(object):
    def __init__(self, testResult):
        self.testResult = testResult


class PassNotification(Notification):
    def __init__(self, testResult):
        super(PassNotification, self).__init__(testResult)
        

class FailNotification(Notification):
    def __init__(self, testResult):
        super(FailNotification, self).__init__(testResult)
