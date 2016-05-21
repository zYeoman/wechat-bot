# encoding:utf-8

import httplib2
import os

from apiclient import discovery
from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import client
from oauth2client import tools
import mimetypes

import threading


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRET_FILE = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                                  'client_secret.json')
APPLICATION_NAME = 'Wechat_bot'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'Wechat_bot.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # response = flow.step1_get_authorize_url('oob')
        credentials = tools.run_flow(flow, store, None)
        print('Storing credentials to ' + credential_path)
    return credentials


def insert_file(service, parentname, filename, path, send):
    """
    Insert file in google drive
    :param service: Google Drive service
    :param parentname: Drive folder
    :param filename: Drive filename
    :param path: local file path
    """
    q = u"name = '{}'".format(parentname)
    results = service.files().list(q=q).execute()
    if not results.get('files'):
        file_metadata = {
            'name': parentname,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata,
                                        fields='id').execute()
    else:
        folder = results.get('files')[0]
    folder_id = folder.get('id')
    fields = u'id, mimeType, name, webViewLink'
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    mime = mimetypes.types_map.get(os.path.splitext(filename))
    media = MediaFileUpload(path,
                            mimetype=mime,
                            resumable=True)
    upload = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields=fields).execute()
    return upload

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)


def get_response(msg, send=None, more=False):
    threading.Thread(target=insert_file, args=(
        drive_service,
        'Wechat_bot',
        msg['FileName'],
        msg['Text'],
        send, )).start()
    return None
