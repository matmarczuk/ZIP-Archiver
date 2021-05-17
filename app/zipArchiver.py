import requests
import threading
import os
import zipfile
import enum

import settings
    
class ZipArchiver:
    def __init__(self, name, urlList):
        self.name = name
        self.urlList = urlList
        self.thread = threading.Thread(target=self.create_archive, name=self.name)

    def __del__(self):
        pass

    def start_processing(self):
        self.thread.start()

    def send_webhook(self):
        webhookUrl = os.getenv('WEBHOOK_URL')
        if webhookUrl :
            link = settings.HOSTNAME + "/archive/get/" + self.name + ".zip"
            r = requests.post(webhookUrl, json = {"link": link })

    def create_archive(self):
        self.archivePath = settings.OUTPUT_DIR + self.name + ".zip"
        for url in self.urlList:
            r = requests.get(str(url), stream=True)
            z = zipfile.ZipFile(self.archivePath, "a", zipfile.ZIP_DEFLATED)
            z.writestr(os.path.basename(url), r.content)
        os.remove(settings.IN_PROGRESS_DIR + self.name)
        self.send_webhook()