from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes

SCOPES = ('https://www.googleapis.com/auth/calendar.readonly ' + 'https://www.googleapis.com/auth/gmail.send')

def SendMessage(service, user_id, message):
    # https://stackoverflow.com/questions/46668084/how-do-i-properly-base64-encode-a-mimetext-for-gmail-api
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    return message

def CreateMessage(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  # To not have you're messages be marked as unimportant
  # https://developers.google.com/gmail/api/v1/reference/users/messages/modify
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# Instead of using credentialing(), can use code below
# def _build_service():
#    scope = 'https://www.googleapis.com/auth/calendar.readonly'
#    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
#        keyfile_dict=app.config.get("SERVICE_ACCOUNT_INFO"),
#        scopes=scope)
#    service = discovery.build('calendar', 'v3', credentials=credentials)
#    return service


def credentialing():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
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
    return creds

def main():
    creds = credentialing()
    service = build('calendar', 'v3', credentials=creds)
    bodyMSG = ""

#### Call the Calendar API
    now = datetime.datetime.utcnow()
    noww = datetime.datetime.utcnow().isoformat() + 'Z'
    then = now + datetime.timedelta(days=1)
    thenn = then.isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=noww, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    print('Checking next events for the next 24 hours')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if thenn.split('T')[0] in start or noww.split('T')[0] in start:
            bodyMSG+= "* " + start.split('T')[1].split('-')[0] + ' ' + event['summary'] + '\n'
    if not bodyMSG:
        bodyMSG = "You have nothing on your calendar for today.\n Have a great day!"
        print(bodyMSG)

#### Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    dateObj = datetime.date.today()
    msgSubject = "Calendar Agenda for " + str(dateObj.month) + '/' + str(dateObj.day) + '/' + str(dateObj.year)
    SendMessage(service,'me',CreateMessage(os.environ['EMAIL'], os.environ['EMAIL'], msgSubject, bodyMSG))

if __name__ == '__main__':
    main()
