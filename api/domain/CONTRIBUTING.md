# Package `domain`
The modules of this package contain two different function types:

* Case 1 : these are ** pure ** functions, that is to say which offer referential transparency
* Case 2 : these are ** impure ** functions, which call on past `repository` functions in parameter (ʻarg` or `kwarg`)

That is, for two calls with the same values ​​returned by the `repository` functions,
the functions of `domain` should return the same results.

Their goal is always to implement management rules which model the "business domain" of the application.

## Do
These functions must contain: calls to `domain`, or` repository` functions as well as the various _HTTP status codes_ that we wish to return.

## Don't
These functions must not contain: _queries_ to the database, calls to web services, or whatever
whatever is considered an I / O. These ʻI / O functions` can be used by a `domain function` provided
whether they are properly injected (i.e. as a function argument, a function keyword-argument or a class constructor).

## Testing
These functions are unit tested and do not require _mocking_ or instantiation of the database or a Flask context. These tests must be extremely quick to run and are generally excellent ground. training for Test Driven Development (TDD).

Their objectives include:
* list the behaviors and responsibilities of a function
* list the "business" exceptions that a function is likely to throw
* give examples of the execution of a function


## For more information
* https://fr.wikipedia.org/wiki/Transparence_r%C3%A9f%C3%A9rentielle
* We call an `I / O function` any function that depends on a system external to its execution context. For example:
  * a file system
  * a database
  * server clock
  * the network
  * a light sensor
  * etc.
