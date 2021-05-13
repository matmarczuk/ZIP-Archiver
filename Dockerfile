FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install validators requests
COPY ./app /app