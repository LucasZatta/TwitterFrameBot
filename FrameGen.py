from __future__ import print_function
import random
import io
import time
import os.path
import cv2
from googleapiclient import discovery

import google.oauth2.service_account as ServiceAccountCredentials

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import tweepy

TYPEVIDEO = 'video/x-matroska'

JSONPATH = 'JSONPATH'

SCOPES = ['https://www.googleapis.com/auth/drive']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def createServiceObject():
    creds = None
    creds = ServiceAccountCredentials.Credentials.from_service_account_file(JSONPATH)

    service = discovery.build('drive', 'v3', credentials=creds)

    return service


def downloadVideo(service):
    results = service.files().list().execute()
    items = results.get('files', [])


    index = 0
    while ((('{0}'.format(items[index]['mimeType'])) != TYPEVIDEO)):
    	index = random.randrange(0, len(items))
        #Loops until file corresponding to index matches specified type/format(in this case mkv)


    file_id = ('{0}'.format(items[index]['id']))
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    
    episodeName = 'episode' + str(index) + '.mkv'

    while done is False:
        status, done = downloader.next_chunk()
        #print ("Download %d%%." % int(status.progress() * 100))

    with io.open(episodeName, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())
        #Downloads the video
    return episodeName

def getFrame(episodeName):
    name = '/home/Zvttx/'
    path = name + episodeName
    cap = cv2.VideoCapture(path)

    amountOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameSeq = random.randrange(500, amountOfFrames,1)
    cap.set(1, frameSeq-1)
    #Using the downloaded video, selects a random frame from the total amout of frames of the video
    ret, frame = cap.read()

    fileName = 'jorel_Frame'+str(frame_seq)+'.png'

    cv2.imwrite(fileName, frame)
    #Saves the frame



    os.remove(path)
    #Removes the video to avoid flooding

    cap.release()
    cv2.destroyAllWindows()
    
    return fileName

def uploadFrame(service,fileName):

	folder_id = FOLDERID
	path = '/home/Zvttx/' + fileName

	file_metadata = {'name': fileName, 'parents': [folder_id]}

	media = MediaFileUpload(path,mimetype = 'image/png',resumable = True)
	file = service.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
    #Uploads the saved frame to the Google Drive
	os.remove(path)
    #Removes the image to avoid flooding



def lastCall(service):
	x = 0
	while x <= 23:
		episodename = downloadVideo(service)
		fileName = getFrame(episodename)
		uploadFrame(service,fileName)
		x = x+1
        #Repeats the proccess 24 times(1 frame for each hour of the day)

service = createServiceObject()
lastCall(service)
