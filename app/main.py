from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field


class UrlList(BaseModel):
    urls: List[str] = Field(..., min_items=1)

app = FastAPI()

@app.post("/api/archive/create")
async def create_archive(urlList: UrlList):
    return urlList

@app.get("/")
def read_root():
    return {"Hello": "World"}