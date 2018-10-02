# Blockchain; personal, custom 
Create (or add to existing) blockchain of randomised strings as data; blocks made up of index, datetime, data, previous block hash and current block hash.

## Version 1.1.0, October 2018
Create or add to an existing Blockchain; chain name provided by the user which is stored in a Postgres database.

The next version will:
* allow a user to upload from a file as data as opposed to random strings
* tested as a module import
* custom exception handling

## Version 1.0.0, September 2018
Blockchain in the example is a list, on my machine it saves to a Postgres database.

The next version will create or update a persistent blockchain with data specified by the user.

## Dependencies

### Python
* Python 3.6.5
* Psycopg2 2.7.5

## Run
* Requires Postgres
* Edit module variables relating to database config / connection
* main.py (import or run)

#### Author
* James Chadwick, 2018
* Inspiration taken from an article written in Python 2.7 by Gerald Nash, http://www.aunyks.com/
