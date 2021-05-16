FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install validators requests aiofiles 
COPY ./app /app
RUN mkdir /zip_archive