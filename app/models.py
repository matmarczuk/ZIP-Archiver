from pydantic import BaseModel, Field, validator
import validators
import requests
from typing import List
from fastapi import HTTPException

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
                except requests.exceptions.RequestException:
                    unreachableUrls.append(url)
            else:
                incorrectUrls.append(url)
        
        if incorrectUrls:
            errorMsg = errorMsg + "Some of sent urls have incorrect format " + str(incorrectUrls) + " Please check it and try again "
        if unreachableUrls:
            errorMsg = errorMsg + "Some of sent urls are unreachable " + str(unreachableUrls) + " Please check it and try again "
        if errorMsg:
            raise HTTPException(status_code = 422, detail = errorMsg)
        return urls