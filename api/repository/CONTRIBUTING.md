# Package `repository`

The modules in this package contain functions that implement SQL Alchemy queries based on SQL Alchemy Models defined in the `models` package or reading environment variables (the environment being an external dependency on the system).

## Do

These functions should only contain queries to the database that return either "primitive" data tuples (e.g. a list of e-mail addresses) or instances of SQL Alchemy models. We can also have functions which return a "subset" of queries, that is to say (private) functions that build queries which are not triggered (ie which do not have an `.all()` or `.first()`). 

Type indications will be used in the function signatures to indicate what data is expected at input and output.

## Don't

These functions must not contain:

- Notions relating to `routing` (e.g. HTTP _status codes_, HTTP verbs);
- Management rules;
- Calls to web services.

## Testing

These functions are tested in a Flask context, therefore with a connection to the database. We consider these integration tests. These tests trigger real SQL queries and require data to be present in the database. These tests use the `@clean_database` decorator which takes care of emptying each table before executing a test and insert the necessary data in their `# given` part.

They aim to:

- Verify that a request does what it says and returns the correct data;
- Verify that the queries handle the boundary cases well via expected exceptions.

## For more information

- http://flask-sqlalchemy.pocoo.org/2.3/queries/

## Notes on tsvector functions within keywords.py file

tsvector (text search vector) is a data type which consists of the following characteristics:

- a sorted list (alphabetically)
- normalized words to merge different variants of the same word
- duplicates of same words are removed

Reference: https://stackoverflow.com/questions/42388956/create-a-full-text-search-index-with-sqlalchemy-on-postgresql
