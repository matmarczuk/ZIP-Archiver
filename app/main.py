from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import validators
import json
import requests
import uuid
import weakref
import threading
import time 
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
        self.thread = threading.Thread(target=self.createArchive, name=self.name)

    def start_processing(self):
        self.thread.start()

    def createArchive(self):
        for url in self.urlList:
            r = requests.get(str(url), stream=True)
            z = zipfile.ZipFile("/zip_archive/" + self.name + ".zip", "a", zipfile.ZIP_DEFLATED)
            z.writestr(os.path.basename(url), r.content)
        self.state = StateEnum.COMPLETED

class UrlList(BaseModel):
    urls: List[str] = Field(..., min_items=1)

    @validator("urls")
    def validate_urls(cls, urls):
        incorrectUrls = []
        unreachableUrls = []
        errorMsg = ""

        for url in urls:
            if validators.url(url):
                try:
                    response = requests.head(url)
                    if response.status_code == 200:
                        pass
                    else:
                        incorrectUrls.append(url)
                except requests.exceptions.RequestException as e:
                    unreachableUrls.append(url)
            else:
                incorrectUrls.append(url)
        
        if incorrectUrls:
            errorMsg = errorMsg + "Some of sent urls have incorrect format " + json.dumps(incorrectUrls) + " Please check it and try again "
        if unreachableUrls:
            errorMsg = errorMsg + "Some of sent urls are unreachable " + json.dumps(unreachableUrls) + " Please check it and try again "
        if errorMsg:
            raise ValueError(errorMsg)
        return urls

def generate_hash():
    return str(uuid.uuid4())

app = FastAPI()
zipArchiver = {}

@app.post("/api/archive/create")
async def create_archive(urlList: UrlList):
    archiveHash = generate_hash()
    zipArchiver[archiveHash] = ZipArchiver(archiveHash, urlList.urls)
    zipArchiver[archiveHash].start_processing()
    return {"archive_hash" : archiveHash}

@app.get("/api/archive/status/{archive_hash}")
async def get_status(archive_hash : str):
    try:
        state = zipArchiver[archive_hash].state.value
    except KeyError:
        raise HTTPException(status_code=404, detail="Requested hash no foud")
    return {"status" : state}

@app.get("/")
def read_root():
    return {"Hello": "World"}