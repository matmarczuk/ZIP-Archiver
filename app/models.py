from pydantic import BaseModel, Field, validator
import validators
import requests
from typing import List
from fastapi import HTTPException

import settings


class UrlList(BaseModel):
    urls: List[str] = Field(..., min_items=1)

    @validator("urls")
    def validate_urls(cls, urls):
        incorrectUrls = []
        unreachableUrls = []
        errorMsg = ""
        size = 0
        for url in urls:
            if validators.url(url):
                try:
                    response = requests.head(url)
                    response.raise_for_status()
                    size = size + int(response.headers['Content-length'])
                except requests.exceptions.RequestException:
                    unreachableUrls.append(url)
            else:
                incorrectUrls.append(url)

        if incorrectUrls:
            errorMsg = errorMsg + "Some of sent urls have incorrect format " + str(incorrectUrls) + " Please check it and try again "
        if unreachableUrls:
            errorMsg = errorMsg + "Some of sent urls are unreachable " + str(unreachableUrls) + " Please check it and try again "
        if float(size/10**9) > settings.FILES_MAX_SIZE:
            errorMsg = errorMsg + "Files size sum cannot exceed " + str(settings.FILES_MAX_SIZE) + "GB"
        if errorMsg:
            raise HTTPException(status_code=422, detail=errorMsg)
        return urls
