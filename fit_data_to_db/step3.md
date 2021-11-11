Now we will set up our tables and upload our fit-file.

## Task

First we will have a look at our tables.

`katacoda-scenario-examples/fit_data_to_db/setup.sql`{{open}}

You can see all the tables and columns we need to save or example file (a swimming session).

Edit the last line and insert a user.

Since it is hard to setup python in this environment, we will use a container to insert our file.

Have a look at the Dockerfile `katacoda-scenario-examples/fit_data_to_db/Dockerfile`{{open}}

Lets build and run it!

`docker build -t our-app .`{{execute}}

`docker container run --name our-app --net my-network our-app`{{execute}}

If you are interested how the data is structured and how the insert works, look at the `our_app.py`{{open}} and `example_fit.json`{{open}}.
