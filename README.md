# Flask Template

## Before you start
To install all dependencies

`pip install -r requirements.txt`

To initialize flask-migrate extensions

`flask --app flaskapp db init`

To create initial migration scripts

`flask --app flaskapp db migrate`

To run initial migration scripts

`flask -app flaskapp db upgrade`

## When you're ready
To run the app ( with debug mode on ). For production please use other wsgi servers like Gunicorn etc

`flask --app flaskapp run --debug`