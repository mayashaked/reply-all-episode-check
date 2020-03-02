from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

FROM = 'mayaromyshaked@gmail.com'
TO = 'mayaromyshaked@gmail.com'
SUBJECT = "Is there a new Reply All episode this week?"

def main():

    creds = get_creds()
    service = build('gmail', 'v1', credentials = creds)

    message = create_message(sender = FROM, to = TO, subject = SUBJECT)

    try:
        message = (service.users().messages().send(userId = FROM, body = message).execute())
        print('Message ID %s' % message['id'])
        return(message)
    except HTTPError:
        print('An error occured')


def get_creds():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return(creds)

def create_message(sender = FROM, to = TO, subject = SUBJECT):
    
    msg_text = new_episode_text()

    msg = MIMEText(msg_text)
    msg['subject'] = subject
    msg['from'] = sender
    msg['to'] = to

    return({'raw' : msg.as_string()})



def new_episode_text():

    fp = urllib.request.urlopen('https://gimletmedia.com/shows/reply-all/posts/fyi')
    mybytes = fp.read()

    html = mybytes.decode('utf8')
    fp.close()

    parsed_html = BeautifulSoup(html)

    full_text = parsed_html.body.find('div', attrs={'class' : 'content ctrs-block is-richtext'}).text

    if "No" in full_text:
        return("No :(")
    else:
        return("Yes! :)")




if __name__ == '__main__':
    main()