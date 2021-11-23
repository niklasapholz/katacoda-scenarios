In diesem Schritt werden die Datenbanktabellen erstellt und die Beispiel-Datei in die Datenbank geschrieben.

## Task

Betrachte zuerst die Tabellen-Strukturen.

`katacoda-scenarios/fit_data_to_db/setup.sql`{{open}}

Dies sind alle Tabellen und Spalten die nötig sind, um die Beispiel-Datei zu speichern (in dem Beispiel handelt es sich um ein Schwimmtraining).

Trage in der letzten Zeile einen User ein, um fortzufahren.

Da die Datenbank in einem Container läuft, wird das Python-Script zum Einfügen der Daten ebenfalls in einem Container gestartet.

Bei bestehendem Interesse kann der Dockerfile eingesehen `katacoda-scenarios/fit_data_to_db/Dockerfile`{{open}} und weitere Informationen in der offiziellen Dokumentation nachgesehen werden: https://docs.docker.com/engine/reference/builder/.

Um den Container zu nutzen, muss er zunächst gebaut werden.

`docker build -t our-app .`{{execute}}

Nun kann der Container gestartet werden.

`docker container run --name our-app --net my-network --rm our-app`{{execute}}

Die Datenstruktur des Beispiel-JSONs kann eingesehen werden `katacoda-scenarios/fit_data_to_db/example_fit.json`{{open}}. Das Einfügen in die Datenbank lässt sich anhand des Programmcodes nachvollziehen `katacoda-scenarios/fit_data_to_db/our_app.py`{{open}}.

Bei bestehendem Interesse kann ein PGadmin-Container genutzt werden, um die Ergebnisse in der Datenbank zu betrachtet. Dies setzt minimale SQL-Kenntnisse voraus.

`docker container run -p 80:80 --name pg -e PGADMIN_DEFAULT_PASSWORD=supersicher -e PGADMIN_DEFAULT_EMAIL=max.mustermann@gmx.de --net my-network -d dpage/pgadmin4`{{execute}}

Um auf PGadmin zuzugreifen, kann im Terminalfenster die Optione `View HTTP port 80 on Host 1` ausgewählt werden. Die Nutzerdaten sind im obigen Docker-Commando angegeben. Die Verbindung zum Datenbankserver benötigt folgende Daten host: database, user: postgres, password: supersicher.