# Blockchain; personal file integrity checker
Create (or add to an existing) blockchain of a users text files; blocks made up of index, datetime, data (a variable buffer size of text file data), previous block hash and current block hash.



##### Notes:
* I've generally adhered to PEP8, there are some deviations for sake of readability or showing multiple methods to perform a task i.e. string concatenation.
* Developed on Linux, not tested to any great degree on other OS's.

## Version 1.2.0, October 2018
Uses text files for input data, providing a basic file integrity check; takes up to 10 text files from a data folder.

The next version will

* allow a user to upload a variety of file types and quantities
* be tested as a module import

## Version 1.1.0, October 2018
Create or add to an existing Blockchain; chain name provided by the user which is stored in a Postgres database.

The next version will

* allow a user to upload from a file as data as opposed to random strings
* be tested as a module import

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
