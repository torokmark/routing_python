
import re
from urllib import parse
from routing.exceptions import NoMethodFoundError, NoRouteFoundError, RouteNotValidError, QueryNotValidError

PATH_PARAM_PATTERN = '^{([a-zA-Z0-9]+)}$'
PATH_PART_PATTERN = '^[a-zA-Z0-9\-]+$'

QUERY_KEY_PATTERN = '^[a-zA-Z0-9]+$'
QUERY_VALUE_PATTERN = '(^[a-zA-Z0-9\-@\. ]+$)'

def validate_route_register(route):
    if route.startswith('/'):
       route_parts = get_route_parts(route)
       for part in route_parts:
           if not (re.match(PATH_PART_PATTERN, part) or re.match(PATH_PARAM_PATTERN, part)):
               raise RouteNotValidError()
    else:
        raise RouteNotValidError() 

def validate_route_process(route, query):
    if route.startswith('/'):
        route_parts = get_route_parts(route)
        for part in route_parts:
            if not re.match(PATH_PART_PATTERN, part):
                raise RouteNotValidError()
    else:
        raise RouteNotValidError()

    query = query or {}
    for key in query:
        if not re.match(QUERY_KEY_PATTERN, key) or not re.match(QUERY_VALUE_PATTERN, query.get(key)):
            raise QueryNotValidError()

def get_route_parts(route):
    route = route.rstrip()
    route = route[1:-1] if route.endswith('/') else route[1:]
    route_parts = route.split('/')
    return route_parts

def get_node(siblings, part):
    if part in siblings:
        return siblings[part]
    else:
        return None

def exist(node):
    return node is not None

def is_path_param(part):
    return re.match(PATH_PARAM_PATTERN, part)

def get_resource_path(base, suffix):
    return '{}/{}'.format(base, suffix)

def path_param_exist(siblings):
    for part in siblings:
        if is_path_param(part):
            return True
    else:
        return False

def get_path_param(siblings):
    for part in siblings:
        if is_path_param(part):
            return part
    else:
        return None

def clean_up_path_param(param):
    return re.match(PATH_PARAM_PATTERN, param).group(1)

def route_only(route):
    return route if route.find('?') == -1 else route[0:route.find('?')]

def query_only(route):
    return '' if route.find('?') == -1 else route[route.find('?') + 1:]

def merge_params(query_part, path_params, whitelist):
    query_params = query_part or {}
    query_params = dict((k, parse.unquote(query_params.get(k))) for k in whitelist if k in query_params)
    params = { **path_params, **query_params }
    return params



