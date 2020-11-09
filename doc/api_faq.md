# API FAQ

## How to get authenticate using token?

```bash
curl -X POST -d '{"username": "<username>","password": "<password>"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/api/get_token/
```

## How to perform API queries?
```bash
curl -H 'Authorization: Token <token>' http://127.0.0.1:8000/api/stats/
```
