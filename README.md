# generate-id
A microservice helper that calls the ROR API to do various administrative tasks

## Dev setup

Start generate-id, ror-api and elasticsearch containers

```docker-compose up -d```

To work with ROR data, first create the index:

```docker-compose exec ror-api python manage.py createindex```

To work with the S3 buckets, please enter the name of the S3 bucket and AWS credentials as env vars for the ror-api service in docker compose. This can also be done as a `.env` file.

Optionally, index ROR data into elasticsearch:

```curl localhost:5000/indexdata/<<directory on S3 bucket>>```


## Run tests

```docker exec generate-id python -m pytest```
