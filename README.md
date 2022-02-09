# generate-id
A microservice helper that calls the ROR API to do various administrative tasks

# Dev setup

```docker-compose up```

# Run tests

1. Access the CLI for the generateid container

        docker ps
        docker exec -it [CONTAINER_ID] bash

2. Move to the generateid dir

        cd generateid

3. Run tests

        python -m pytest