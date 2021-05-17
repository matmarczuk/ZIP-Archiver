from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

import uuid
import os

from models import UrlList
from zipArchiver import ZipArchiver
import settings

app = FastAPI()

@app.on_event("startup")
async def check_for_unfinished():
    fileList = os.listdir(settings.IN_PROGRESS_DIR)
    if(fileList) :
        for file in fileList:
            if os.path.isfile(settings.OUTPUT_DIR + file + ".zip") :
                os.remove(settings.OUTPUT_DIR + file + ".zip")
            with open(settings.IN_PROGRESS_DIR + file) as f:
                urls = f.read().splitlines()
            zipArchiver = ZipArchiver(file, urls)
            zipArchiver.start_processing()

@app.post("/api/archive/create")
async def create_archive(urlList: UrlList):
    archiveHash = str(uuid.uuid4())
    zipArchiver = ZipArchiver(archiveHash, urlList.urls)
    urlFile = open(settings.IN_PROGRESS_DIR + archiveHash, "w")
    for url in urlList.urls:
        urlFile.write(url + "\n")
    urlFile.close()

    zipArchiver.start_processing()
    return {"archive_hash" : archiveHash}

@app.get("/api/archive/status/{archive_hash}")
async def get_status(archive_hash : str):
    if os.path.isfile(settings.IN_PROGRESS_DIR + archive_hash):
        return {"status" : "in-progress"}
    elif (os.path.isfile(settings.OUTPUT_DIR + archive_hash + ".zip") and (os.path.isfile(settings.IN_PROGRESS_DIR + archive_hash) is False)) :
        return {"status" : "completed", "url" : settings.HOSTNAME + "/archive/get/" + archive_hash + ".zip"}
    else:
        raise HTTPException(status_code = 404, detail = "Requested archive hash no foud")

@app.get("/archive/get/{file_name}")
async def get_archive(file_name : str):
    filePath = settings.OUTPUT_DIR + file_name
    if not os.path.isfile(filePath):
        raise HTTPException(status_code = 404, detail = "File not found")
    return FileResponse(filePath)