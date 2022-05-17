# Python Marshmallow

Python Marshmallow tutorial for HTTP Request Body JSON parsing & validation


* Start the server
```bash
(venv) $ python app.py
```

* To invoke API through `curl` command

```bash
$ curl 
    --request POST 
    --data '@request-body.json' 
    --header 'Content-Type: application/json' 
    'http://localhost:5000/project'
```