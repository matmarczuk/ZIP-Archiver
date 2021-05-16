# ZIP Archiver
Project of web app that creates a (zip) archive from
multiple publicly accessible files. Creating of zip archive is done in parallel. User can check progress status, and once its completed it gets link to download generated archive.

### Fast run 
`docker build -t myimage .`
`docker run -d -p 80:80 -e MAX_WORKERS="1" myimage`
* `MAX_WORKERS` is param used by FastAPI to limit number of running workers (parallel processes). 
In this simple app due to usage of processing variables stored locally it has to be set to 1.

## Endpoints 
### ``POST`` /api/archive/create
* Request body (example)
```
{
    "urls":[
        "https://some_public_link_to_jpg_file.jpg",
        "https://some_public_link_to_png_file.png",
        "https://some_public_link_to_pdf_file.pdf"
    ]
}
```
* Success Response (example)

Code ``200``: 
```
{
    "archive_hash": "7da6e067-a780-41af-96d0-cf0e0cc02f6a"
}
```

* Error Response (example)

Code ``422``:
```
{
    "detail": "Some of sent urls have incorrect format ['htt://my.jpg'] Please check it and try again "
}
```
### ``GET`` /api/archive/status/{hash_id}
* Success Response

Code ``200``: 
```
{
    "status": "in-progress"
}
```
Once completed, response is extended with url to generated archive
```
{
    "status": "completed",
    "url": "http://localhost/archive/get/3c5350f5-c43d-4c5b-9810-e09c47045290.zip"
}
```

* Error Response 

Code ``404``:
```
{
    "detail": "Requested archive hash no foud"
}
```

