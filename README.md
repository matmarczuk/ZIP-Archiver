# ZIP Archiver
Project of web app that creates a (zip) archive from
multiple publicly accessible files. Creating of zip archive is done in parallel. User can check progress status, and once its completed it gets link to download generated archive.

Features: 
* Limit (summary) maximum files size 
* Check url syntax and link availability
* Regenerate archive that was corrupted by server restart (during in-progress state)
* Send webhook once archive was generated 
* Delete archive after download 

## Fast run 
`docker build -t <my-img-name> .`

`docker run -d -p 80:80 WEBHOOK_URL=<webhook-url> <my-img-name>`

where 
`WEBHOOK_URL` - Adress of another server that will receive POST with following body after successful archive generation
```
{
    "link" : "http://localhost/archive/get/3c5350f5-c43d-4c5b-9810-e09c47045290.zip"
}
```
### Settings
Settings are defined in settings.py file

* `IN_PROGRESS_DIR` - directory on the server where processing data are stored (default = "/in-progress/")
* `OUTPUT_DIR` - directory on the server where files archives are stored (default = "/zip_archive/")
* `HOSTNAME` - name of the server (default - "http://localhost")
* `FILES_MAX_SIZE` - maximum summary size of files which are going to be archived  (default = 2.0 # GB)

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
**After downloading archive will be removed from server!**

* Error Response 

Code ``404``:
```
{
    "detail": "Requested archive hash no foud"
}
```

