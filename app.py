#!/usr/bin/env python

import sys
from datetime import date, datetime
import json

from routing import routing
from resources import users
from routing.exceptions import QueryNotValidError, NoMethodFoundError, NoRouteFoundError, RouteNotValidError

def handler(event, context):

    response = {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": ''
    }

    routing.register(route='/users/', 
                     callback=(lambda: users.list_users()))

    routing.register(route='/users', 
                     callback=(lambda name, email: users.create_user(name, email)),
                     method=routing.Methods.POST,
                     params={'name', 'email'})

    routing.register(route='/users/{id}', 
                     callback=(lambda id: users.get_user(id)), 
                     method=routing.Methods.GET)
    
    routing.register(route='/users/{id}', 
                     callback=(lambda id: users.delete_user(id)),
                     method=routing.Methods.DELETE,
                     params={'id'}) # pathparams are not needed to be defined as queryparams

    routing.register(route='/users/{id}', 
                     callback=(lambda id, name, email: users.update_user(id, name, email)),
                     method=routing.Methods.PUT,
                     params={'name', 'email'}) # pathparams are not needed to be defined as queryparams


    try:
        body = routing.process(event.get('path'), event.get('queryStringParameters'), event.get('httpMethod'))
        response['body'] = json.dumps(body, default=str)
    except (RouteNotValidError, QueryNotValidError) as err:
        response['statusCode'] = 400
        response['headers']['error'] = err.message
    except NoMethodFoundError as err_no_meth:
        response['statusCode'] = 405
        response['headers']['error'] = err_no_meth.message
    except NoRouteFoundError as err_no_rou:
        response['statusCode'] = 404
        response['headers']['error'] = err_no_rou.message
    return response


if __name__ == '__main__':
    print('GET ALL:', handler({
        'path': '/users/',
        'httpMethod': 'GET'
    }, None))
    print('POST:', handler({
        'path': '/users/',
        'queryStringParameters': {
            'name': 'Name comes here',
            'email': 'email@example.com'
        },
        'httpMethod': 'POST'
    }, None))
    print('GET', handler({
        'path': '/users/1',
        'httpMethod': 'GET'
    }, None))
    print('PUT', handler({
        'path': '/users/1',
        'queryStringParameters': {
            'name': 'Another name comes here',
            'email': 'email@example.com'
        },
        'httpMethod': 'PUT'
    }, None))

    print('GET ALL:', handler({
        'path': '/users/',
        'httpMethod': 'GET'
    }, None))

    print('DELETE:', handler({
        'path': '/users/1',
        'httpMethod': 'DELETE'
    }, None))

    print('GET ALL:', handler({
        'path': '/users/',
        'httpMethod': 'GET'
    }, None))

