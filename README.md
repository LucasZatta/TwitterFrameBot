# TwitterFrameBot
Python Bot that posts an image on a Twitter Account every 1 hour.

## **Overview**

The objective while making this bot was to build what I called a "Frame Bot". The idea was to have a Twitter account post a frame from the brazilian animated series **Irmão do Jorel** every one hour(really good show chek it out!).

Using Google Drive API and Twitter API the bot can download images from the drive and upload them on a Twitter account.

### Frame.py

The episodes are stored in the Drive as .mkv files. This first script(hosted on [PythonAnywhere](https://www.pythonanywhere.com), selects a random video file and Downloads it using the Google Drive API. Using OpenCV, it save a random frame from the episode and uploads it to the Drive.
After uploading the frame to the drive, both the frame and the video get deleted from the PythonAnywhere file manager to avoid flooding.

This script runs daily and uploads 24 frames to the Drive(one for every hour of the day).

### PostBot.py

This script(hosted on [Heroku](https://www.heroku.com) uses the Google Drive API to select a random image file(the random frame uploaded with the previous script) and downloads it. Then, using the Twython lib to access the Twitter API, the image downloaded is uploaded to the account timeline as a Tweet.
Right after a image is tweeted, it is also removed from the drive, in order to avoid flooding and repeated images being tweeted.

To achieve the "hourly" effect, the script uses time.sleep(3600). The parameters are in seconds, and can be changed to achieve the desired time interval.

### Heroku Environmental Variables

To use the Twitter API, 4 keys are required to complete the authentication proccess. These keys should **not** be hardcoded on your script by any means, as they give total access to the Twitter Account linked to them. Deploying the script on Heroku, it's possible to create environmental variables, and use os.environ[] or os.getenv() to access them without exposing them to whoever access your git repo.

The same applies to the Google Drive API, only difference being that the variable is a .JSON.

## Why use 2 hosts and 2 scripts?
Python Anywhere can download the video files to its file manager in a way that their paths can be used as parameters to OpenCV method "captureVideo". The video files were originally kept in the PythonAnywhere file manager itself, but it has a storage limit for free users. And that's where the Google Drive API comes in handy.
By using it to download one video at a time(and deleting after using it to avoid flooding), it can "produce" frames and upload them to the Google Drive, where the second script hosted on Heroku.com can access the frames and upload them(and then also delete them from the drive to avoid flooding). The second script is always-on-task.

##  The Bot
## You can find the bot [here!](https://twitter.com/BotJorel)

![jorel](joreLFrame.jpeg)  

Thanks for reading!
