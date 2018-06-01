import os
import sys
import subprocess
import smtplib
from email.mime.text import MIMEText

def send(server, file, fr, to):
        try:
                with open(file) as f:
                        msg = MIMEText(f.read())
                msg['Subject'] = 'Mail Queue Address List'
                msg['From'] = fr
                msg['To'] = to
                send = smtplib.SMTP(server, 25)
                send.send_message(msg)
                s.quit()
        except:
                print('Mail could not sent...')
def wr_post(word):
        buffer = 'buffer.txt'
        ma = ''
        with open(buffer, "w", encoding = "ISO-8859-1") as myfile:
            myfile.write(str(word))
        with open(buffer, "r") as bfile:
                for line in bfile.readlines():
                        if 'To:' in line:
                                ma = line
        return ma
def wr_addr(wfile, word):
        with open(wfile, "a+") as myfile:
            myfile.write(word + "\n")
def get_queue():
        get = subprocess.Popen(["mailq"], stdout = subprocess.PIPE, universal_newlines=True)
        output, err = get.communicate()
        pr_queue = output
        queue = []
        for pr in pr_queue.splitlines():
                strip = pr[0:11]
                strip = strip.strip()
                if len(strip) == 10:
                        queue.append(strip)
        return queue

def parse_email():
        address = ''
        contents = get_queue()
        wr_file = 'invalid-mail.txt'
        for content in contents:
                post = subprocess.Popen(["postcat", "-vq", content], stdout = subprocess.PIPE, universal_newlines=True)
                output, err = post.communicate()
                address = wr_post(output)
                wr_addr(wr_file, address)
        return wr_file
def queue_main(server, fr, to):
        try:
                get = parse_email()
                send(server, get, fr, to)
        except OSError as err:
                print('OS error: {0}'.format(err))
        except ValueError as err:
                print('Value error: {0}'.format(err))
        except:
                print('Unexcepted error:', sys.exc_info()[0])
                raise
if __name__ == "__main__":
        try:
                server = sys.argv[1]
                fro = sys.argv[2]
                to = sys.argv[3]
                queue_main(server, fro, to)
        except:
                print('Unexcepted error:', sys.exc_info()[0])