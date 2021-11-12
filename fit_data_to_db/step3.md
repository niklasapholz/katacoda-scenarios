Now we will set up our tables and upload our fit-file.

## Task

First we will have a look at our tables.

`katacoda-scenarios/fit_data_to_db/setup.sql`{{open}}

You can see all the tables and columns we need to save or example file (a swimming session).

Edit the last line and insert a user.

Since it is hard to setup python in this environment, we will use a container to insert our file.

Have a look at the Dockerfile `katacoda-scenarios/fit_data_to_db/Dockerfile`{{open}}

Lets build and run it!

`docker build -t our-app .`{{execute}}

`docker container run --name our-app --net my-network --rm our-app`{{execute}}

If you are interested how the data is structured and how the insert works, look at the `our_app.py`{{open}} and `example_fit.json`{{open}}.

You can see the results with another container if you can want to.

`docker container run -p 80:80 --name pg -e PGADMIN_DEFAULT_PASSWORD=supersicher -e PGADMIN_DEFAULT_EMAIL=max.mustermann@gmx.de --net my-network -d dpage/pgadmin4`{{execute}}

Open the host with the Terminal-Plus-Symbol and use the user and password provided by the run command. Connect to the database with host: database, user:postgres, password: supersicher. Now you can have a look at all tables.
