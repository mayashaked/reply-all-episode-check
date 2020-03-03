import smtplib
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

SENDER_ADDRESS = # your Gmail address
SENDER_PASS = # your Gmail password
RECEIVER_ADDRESS = # your Gmail address or the address you want to email

def main():

    message = create_message()

    pass


def create_message(sender_address = SENDER_ADDRESS, sender_pass = SENDER_PASS, 
    receiver_address = RECEIVER_ADDRESS):
    
    mail_content = new_episode_text()

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Is there a new Reply All episode this week?'

    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    pass


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
