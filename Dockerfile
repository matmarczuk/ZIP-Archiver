FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install validators requests zipstream-new aiofiles 
COPY ./app /app
RUN mkdir /zip_archive