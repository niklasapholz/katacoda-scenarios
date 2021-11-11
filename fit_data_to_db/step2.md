Now it is time to get our PostgreSQL up and running. Since we do not want install postgres and all its dependencies, we will use docker container.

## Task

First we create a network for the container communicate.

`docker network create -d bridge my-network`{{execute}}

Than we start our database.

`docker container run --name database -e POSTGRES_PASSWORD=supersicher --net my-network -d postgres:14.0`{{execute}}

You can check whether the database is running with

`docker ps`{{execute}}

and check the logs with

`docker logs -f database`{{execute}}

Next we will write our fit-data to the database.