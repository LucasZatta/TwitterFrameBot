from __future__ import print_function
import random
import io
import os
import time
import google.oauth2.service_account as ServiceAccountCredentials
import json
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from twython import Twython
from PIL import Image

TYPEPNG = 'image/png'


SCOPES = ['https://www.googleapis.com/auth/drive']

def createService():
    #Geting Json variable from Heroku enviromental variables
    json_creds = os.getenv('CREDENTIAL_JSON')

    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.Credentials.from_service_account_info(creds_dict)


    service = discovery.build('drive', 'v3', credentials=creds)

    return service

def createTwitterauth():

    #Creating Twython object. Used to interact with the Twitter API
    #Once again using Heroku enviromental variables
    APP_KEY = os.environ['APP_KEY']
    APP_SECRET = os.environ['APP_SECRET']
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

    twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    return twitter

def postFrame(service,twitter):

    results = service.files().list().execute()
    items = results.get('files',[])
    index = 0
    while ((('{0}'.format(items[index]['mimeType'])) != TYPEPNG)):
        index = random.randrange(0, len(items))
        #Loops until the file corresponding to the index matches the specified type(in this case a png)


    file_id = ('{0}'.format(items[index]['id']))
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while done is False:
        status, done = downloader.next_chunk()

    img=Image.open(fh)
    blob = io.BytesIO()
    img.save(blob, 'JPEG')
    blob.seek(0)
    #Downloads file from Google Drive using buffer then save it on a blob

    response = twitter.upload_media(media=blob);

    twitter.update_status(status='', media_ids=[response['media_id']])
    #Upload the image as a Tweet using the Twython object

    deleteFile(service,file_id)
    #Delete file to avoid flooding your Drive and uploading repeated frames


def deleteFile(service,fileID):

    service.files().delete(fileId=fileID).execute()
    
def main():
    #The objective was to post a frame per hour, hence the time.sleep set to 3600 seconds
    service = createService()
    twitter = createTwitterauth()
    while True:
        postFrame(service, twitter)
        time.sleep(3600)

if __name__ == '__main__':
    main()