import requests
import threading
import os
import zipfile
import enum

class StateEnum(enum.Enum):
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    ERROR = "error occured"
    
class ZipArchiver:
    def __init__(self, name, urlList):
        self.name = name
        self.state = StateEnum.IN_PROGRESS
        self.urlList = urlList
        self.thread = threading.Thread(target=self.create_archive, name=self.name)

    def start_processing(self):
        self.thread.start()

    def send_webhook(self):
        webhookUrl = os.getenv('WEBHOOK_URL')
        if webhookUrl :
            link = "localhost/archive/get/" + self.name + ".zip"
            r = requests.post(webhookUrl, json = {"link": link })

    def create_archive(self):
        self.archivePath = "/zip_archive/" + self.name + ".zip"
        for url in self.urlList:
            r = requests.get(str(url), stream=True)
            z = zipfile.ZipFile(self.archivePath, "a", zipfile.ZIP_DEFLATED)
            z.writestr(os.path.basename(url), r.content)
        self.state = StateEnum.COMPLETED
        self.send_webhook()