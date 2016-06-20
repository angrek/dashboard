#!/home/wrehfiel/ENV/bin/python2.7
#########################################################################
#
# Script to check the size of the esb console.log files
#
# Boomer Rehfield - 8/7/2014
#
#########################################################################

from ssh import SSHClient
import smtplib
from email.mime.text import MIMEText
import email.utils


def update_server():
    text = "======================ESB /opt Console Space Report=============\n"
    print text

    server_list = ['p1esbapp', 'p2esbapp', 'p3esbapp', 'p4esbapp', 'p5esbapp', 'p6esbapp', 'p7esbapp', 'p8esbapp', 'p9esbapp', 'p10esbapp', 'p11esbapp', 'p12esbapp']
    for server in server_list:
        text = text + "-------------------" + str(server) + "---------------------\n"
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(str(server), username="wrehfiel")

        command = 'df -h | grep opt; du -csh /opt/esb/jboss-eap-4.3/jboss-as/console.log'
        stdin, stdout, stderr = client.exec_command(command)
        for output in stdout.readlines():
            # print output
            text = text + output + '\n'
    print text

    # message = """From: Boomer <william.rehfield@wellcare.com>
    # To: Boomer <william.rehfield@wellcare.com>
    # Suject: ESB /opt console.log Report.""" + text
    msg = MIMEText(text)
    msg['Subject'] = 'ESB /opt console.log report'
    msg['From'] = email.utils.formataddr(('Boomer', "william.rehfield\@wellcare.com"))
    msg['To'] = email.utils.formataddr(('Boomer', "william.rehfield\@wellcare.com"))

    # s = smtplib.SMTP('localhost')
    # s.sendmail(

    server = smtplib.SMTP('mail')
    server.sendmail("william.rehfield@wellcare.com", "william.rehfield@wellcare.com", msg.as_string())


if __name__ == '__main__':
    print "Running..."
    # print timezone.now()
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    update_server()
    # print timezone.now()
