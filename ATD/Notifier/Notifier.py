
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Notify(object):
    def __init__(self):
        pass

    def send_notification(self, email, failed, passed):
        """
        Displays passed and failed tests. Sends an email if there are any failed tests.
        :param email: email address to send failed tests to.
        :param failed: list of failed Notifications
        :param passed: list of passed Notifications
        :return:
        """
        print ""
        print "Passed tests: "
        for p in passed:
            print p

        print "Failed tests: "
        for f in failed:
            print f
        if len(failed) > 0:
            self.send_email(email, failed)

    def send_email(self, email, failed):
        """
        Sends a notification email to address `email` with the digests provided in the `failed` list.
        Even if failed is empty, send_email will still try to send an email.
        :param email: email address as a string to send the notification to.
        :param failed: list of failed notifications to put in body of email.
        :return:
        """
  
        sender = "nmsu.cs.team.atd@gmail.com"
        password = "thepasswordforourteam"
        receiver = email

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Errors!"
        msg['From'] = sender
        msg['To'] = receiver

        text = "Hi!\nHere is the errors with your test cases:\n"
        failed = "\n".join(failed)

        text += failed
        part1 = MIMEText(text, 'plain')

        msg.attach(part1)

        s = smtplib.SMTP('smtp.gmail.com:587', timeout=10)
        s.starttls()
        try:
            s.login(sender, password)
            s.sendmail(sender, receiver, msg.as_string())
        finally:
            s.quit()
