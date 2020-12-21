# Webforces

## How to install:
1. Install [Python 3.7+](https://www.python.org/downloads/)
1. Install [MongoDB](https://docs.mongodb.com/manual/installation/)
1. Install gcc compiler and make sure `g++` is in your system PATH.
1. Install webforces:
    ```bash
    python -m pip install -r requirements.txt
    python manage.py migrate
    ```

## How to run:

### Server
```bash
python manage.py runserver
```

### Web application
Open URL that is displayed after starting server in your browser.

### Desktop application
```bash
cd desktop_app
python start_application.py
```
