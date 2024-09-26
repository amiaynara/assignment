## What does this do?
This is a django app.
`http://localhost:8000/api/analysis/1/files/initial-data/?tags=sqlite` tries to access a file from the `s3`. This file is an `sqlite` file.
The goal is to query the file.
---

### Set up:
The django app uses [(sqlite-s3-query)](https://github.com/michalc/sqlite-s3-query), to query the sqlite file on s3.
`.env` file needs to be populated with appropriate credentials, which should have access to the dev account.

```
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```
To test if the setup worked, 
* check the container logs: `docker logs -f django-app`
* On browser, http://localhost:8000/api/analysis/1/files/test

---

### Issues: 
Endpoint: `http://localhost:8000/api/analysis/1/files/initial-data/?tags=sqlite`
When the app is run using the django dev server, the endpoint takes time but eventually returns the expected value.
Also, when we are not using the containerized setup (directly the running the app using `./manage runserver` or `gunicorn`), the endpoint
still returns the expected response(although it takes a lot of time).

But when using `gunicorn`,

1. The query is made more than once (while there is just one call)
2. Or some error happens `unknown error`
```
Internal Server Error: /api/analysis/1/files/initial-data/
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/views/decorators/csrf.py", line 65, in _view_wrapper
    return view_func(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/viewsets.py", line 124, in view
    return self.dispatch(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app/resources/file/main.py", line 40, in initial_data
    result = self.execute_query(file_obj.uri, queries)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app/resources/file/main.py", line 74, in execute_query
    result = [row for row in rows]
                             ^^^^
  File "/usr/local/lib/python3.12/site-packages/sqlite_s3_query.py", line 356, in rows
    raise SQLiteError(libsqlite3.sqlite3_errstr(res).decode())
sqlite_s3_query.SQLiteError: unknown error
```
