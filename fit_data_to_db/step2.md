Nun kann die Datenbank aufgesetzt werden. Um den Arbeitsaufwand überschaubar zu halten, werden im Folgenden Docker-Container benutzt.

## Task

Damit die Container untereinander kommunizieren können, muss zunächst ein Netzwerk aufgesetzt werden.

`docker network create -d bridge my-network`{{execute}}

Danach kann die PostgreSQL-Instance gestartet werden. Dabei ist darauf zu achten, dass sie in dem eben erschaffenen Netzwerk gestartet wird.

`docker container run --name database -e POSTGRES_PASSWORD=supersicher --net my-network -d postgres:14.0`{{execute}}

Kontrolliere ob die Datenbank läuft

`docker ps`{{execute}}

und verfolge die Logs um zu wissen, wann die Datenbank fertig gestartet ist.

`docker logs -f database`{{execute}}

Weiter Informationen bezüglich der Datenbank und des Docker-Images sind unter https://hub.docker.com/_/postgres zu finden.