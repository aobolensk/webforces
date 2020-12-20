# FAQ

## How to create super user to properly use service?
```bash
python manage.py createsuperuser
```

## How to run tests?
Preferable way:
```bash
pytest
pytest --html=report.html  # to create HTML report
pytest --enable_selenium   # to launch Selenium based tests for Web client (see notes below)
pytest --enable_qt         # to launch Qt based tests for Desktop client (see notes below)
````
Alternative:
```bash
python manage.py test
```
There are additional requirements to run Qt based and Selenium based tests:
1. Create superuser using `python manage.py createsuperuser` with username "walrus" and password "wal"
1. Make sure you have started the server using `python manage.py runserver` otherwise all Selenium based tests will fail
1. Create user with username "chifir" and password "thispasswordistooshort" by application or web page

For Selenium based tests also:
1. Download [geckodriver](https://github.com/mozilla/geckodriver/releases)
1. Unarchive it
1. Make sure that geckodriver executable in PATH

## How to use API?
See [API FAQ](./api_faq.md)
