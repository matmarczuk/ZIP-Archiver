from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

import uuid
import os

from models import UrlList
from zipArchiver import StateEnum, ZipArchiver

app = FastAPI()
zipArchiver = {}

@app.post("/api/archive/create")
async def create_archive(urlList: UrlList):
    archiveHash = str(uuid.uuid4())
    zipArchiver[archiveHash] = ZipArchiver(archiveHash, urlList.urls)
    zipArchiver[archiveHash].start_processing()
    return {"archive_hash" : archiveHash}

@app.get("/api/archive/status/{archive_hash}")
async def get_status(archive_hash : str):
    try:
        state = zipArchiver[archive_hash].state
    except KeyError:
        raise HTTPException(status_code = 404, detail = "Requested archive hash no foud")
    if state in (StateEnum.IN_PROGRESS, StateEnum.ERROR):
        return {"status" : state.value}
    elif state is StateEnum.COMPLETED:
        return {"status" : state.value, "url" : "http://localhost/archive/get/" + archive_hash + ".zip"}

@app.get("/archive/get/{file_name}")
async def get_archive(file_name : str):
    filePath = "/zip_archive/" + file_name
    if not os.path.isfile(filePath) :
        raise HTTPException(status_code = 404, detail = "File not found")
    return FileResponse(filePath)