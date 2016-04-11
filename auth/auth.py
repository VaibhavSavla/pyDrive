from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from utility.paths import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = './auth/client_secret.json'
APPLICATION_NAME = 'pyDrive'


def get_credentials(account):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = os.path.join(HOME_DIR, META_DIR, account, "credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'pyDrive.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service(credentials_folder, version='v3'):
    """Get the service object for the drive account

    Args:
        credentials_folder: path to the folder where user credentials are 
                stored
        version: specifies the version of drive api to use ('v2' or 'v3').

    Returns:
        service
    """
    credentials = get_credentials(credentials_folder)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', version, http=http)
    return service
