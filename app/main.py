from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
import validators
import json
import requests

class UrlList(BaseModel):
    urls: List[str] = Field(..., min_items=1)

    @validator("urls")
    def validate_urls(cls, urls):
        incorrectUrls = []
        unreachableUrls = []
        error_msg = ""

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
            error_msg = error_msg + "Some of sent urls have incorrect format " + json.dumps(incorrectUrls) + " Please check it and try again "
        if unreachableUrls:
            error_msg = error_msg + "Some of sent urls are unreachable " + json.dumps(unreachableUrls) + " Please check it and try again "
        if error_msg:
            raise ValueError(error_msg)
        return urls
        
app = FastAPI()

@app.post("/api/archive/create")
async def create_archive(urlList: UrlList):
    return urlList

@app.get("/")
def read_root():
    return {"Hello": "World"}