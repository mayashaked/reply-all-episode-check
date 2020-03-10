#!/usr/local/bin/python3
import smtplib
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import os, sys
import json


def main():

    args = get_args()

    message = create_message(args)

    pass


def get_args():

    with open(os.path.join(sys.path[0], 'configs.txt')) as json_file:
        args = json.load(json_file)

    return(args)

def create_message(args):
    
    mail_content = new_episode_text()

    message = MIMEMultipart()
    message['From'] = args['sender']
    message['To'] = ', '.join(args['receivers'])
    message['Subject'] = 'Is there a new Reply All episode this week?'

    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
    session.starttls() # enable security
    session.login(args['sender'], args['password']) # login with mail_id and password
    text = message.as_string()
    session.sendmail(args['sender'], args['receivers'], text)
    session.quit()

    pass


def new_episode_text():

    fp = urllib.request.urlopen('https://gimletmedia.com/shows/reply-all/posts/fyi')
    mybytes = fp.read()

    html = mybytes.decode('utf8')
    fp.close()

    parsed_html = BeautifulSoup(html, 'html.parser')

    full_text = parsed_html.body.find('div', attrs={'class' : 'content ctrs-block is-richtext'}).text

    if "No" in full_text:

        return("No :(")

    else:

        return("Yes! :)")


if __name__ == '__main__':

    main()
