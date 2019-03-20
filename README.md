# Routing mechanism implemented in python

This is an experimental project about how to approach routing implementation.

Routing consists of two parts, one is the *route register* which used to declare
paths with lambdas and methods and, optionally, query params. The other one is the
*processor* which parse the url, takes the params out of it and returns the
result.

## Define a route

`register` function is available for registering routes. It has four params, which are the followings:
* **route**: define route that can be seen like: `/`, `/users`, `/users/`, 
    `/users/{id}/details/{address_id}/`
* **callback**: lambda function which is executed if request falls on the route
* **method**: can be one of the well-known methods. Default to `GET`
* **params**: list of *queryparams* as a whitelist. Other queryparams wont be processed. 
    Pathparams are optional here.

```python
routing.register(route='/users', 
                 callback=(lambda name, email: users.create_user(name, email)),
                 method=routing.Methods.POST,
                 params={'name', 'email'})

routing.register(route='/users/{id}', 
                 callback=(lambda id: users.get_user(id)), 
                 method=routing.Methods.GET)
```

## Process a call

`process` function takes the following three params and process it. 
The return value is the result of the executed lambda belongs to the route.
* **path**: the route
* **query string params**: dict of query params with their values
* **method**: the method of the call

```python
resp_body = routing.process(event.get('path'), 
                            event.get('queryStringParameters'), 
                            event.get('httpMethod'))
```

`process` raises different kind of errors depending on the error in the path,
query or method.

The following errors can be raised in case of failures.

* **NoRouteFoundError**: raised in case of no registered route found
* **NoMethodFoundError**: raised in case of no registered route found with the
    method
* **RouteNotValidError**: raised when route contains invalid chars
* **QueryNotValidError**: raised when query contains invalid chars

## Response

The response body is the return value of the process function which can be an
object or `None` in case of void return.

## Entrypoint of a call

Considered as one entrypoint given, called `handler`, which requires two
params, an `event` object which contains the abovementioned key-value pairs and
a `context`.

It returns a response object which body is serialized by `json.dump`. Also
contains status code and encoding.

