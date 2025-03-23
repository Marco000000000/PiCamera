#def notify():
#	return
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)
path = "Capture"
def notify():
    for x in os.listdir(path):
        file_list = drive.ListFile(
            {'q': "'16aQKD7u1Uc6OpN5SIOJxzwAM1MbZ2d1A' in parents and trashed = False"}).GetList()
        try:
            for file1 in file_list:
                if file1['title'] == os.path.join(path, x):
                    file1.Delete()
        except:
            pass
        f = drive.CreateFile({'parents': [{'id': '16aQKD7u1Uc6OpN5SIOJxzwAM1MbZ2d1A'}]})
        f.SetContentFile(os.path.join(path, x))
        f.Upload()
        f = None


