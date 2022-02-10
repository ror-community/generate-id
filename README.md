# generate-id
A microservice helper that calls the ROR API to do various administrative tasks

## Dev setup

Start generate-id, ror-api and elasticsearch containers
```docker-compose up -d```

Optionally, index ROR data into elasticsearch
```docker-compose exec web python manage.py setup```


## Run tests

```docker exec generate-id python -m pytest```
