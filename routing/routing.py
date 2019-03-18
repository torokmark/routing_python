
from enum import Enum

from routing.exceptions import NoMethodFoundError, NoRouteFoundError, RouteNotValidError
from routing.executor import execute
import routing.helpers as helpers 


class Methods(Enum):
    GET = 1
    HEAD = 2
    POST = 3
    PUT = 4
    DELETE = 5
    CONNECT = 6
    OTPIONS = 7
    TRACE = 8
    PATCH = 9

    @classmethod
    def get(self, method):
        if hasattr(self, method):
            return self[method]
        else:
            return None



def register(route, callback, method=Methods.GET, params=set()):
    helpers.validate_route_register(route)
    routing_tree.add(route, callback, method, params)

def process(resource_path, query_string_params, method):
    helpers.validate_route_process(resource_path, query_string_params)
    
    meth = Methods.get(method)
    
    callback_with_params, path_params = routing_tree.find(resource_path, meth)
    
    params = helpers.merge_params(query_string_params, path_params, callback_with_params['params']) 
    
    result = execute(callback_with_params['callback'], params) 
    return result 

def put():
    print(routing_tree)


class RoutingTree:
    def __init__(self):
        self.root = Node(value='', resource_path='/')
        
    def add(self, route, callback, method, params):
        if route == '/':
            self.root.callbacks[method] = { 'callback': callback, 'params': params }
        else:
            route_parts = helpers.get_route_parts(route)
            self.__add(self.root.children, route_parts, self.root.value, callback, method, params)

    def find(self, route, method):
        if self.root.value == route.strip()[1:]:
            return self.root.callbacks.get(method), {}
        else:
            route_parts = route.strip().split('/')[1:]
            route_parts = route_parts[:-1] if route.strip().endswith('/') else route_parts
            path_params = {}
            return self.__find(self.root.children, route_parts, method, path_params)

    # private methods:
    def __add(self, siblings, route_parts, parent_resource_path, callback, method, params):
        part = route_parts[0]
        node = helpers.get_node(siblings, part)
        if not helpers.exist(node):
            
            if helpers.is_path_param(part) and helpers.path_param_exist(siblings):
                raise RouteNotValidError('Path param is already defined. Not allowed : {}'.format(part))
            
            resource_path = helpers.get_resource_path(parent_resource_path,part)
            new_node = Node(part, resource_path)
            siblings[part] = new_node
            route_parts = route_parts[1:]
            if len(route_parts) != 0:
                self.__add(new_node.children, route_parts, resource_path, callback, method, params)
            else:
                new_node.callbacks[method] = { 'callback': callback, 'params': params }
        else:
            if len(route_parts) == 1:
                node.resource_path = helpers.get_resource_path(parent_resource_path,part)
                node.callbacks[method] = { 'callback': callback, 'params': params }
            else:
                resource_path = helpers.get_resource_path(parent_resource_path,part)
                node.resource_path = resource_path
                route_parts = route_parts[1:]
                self.__add(node.children, route_parts, resource_path, callback, method, params)

    def __find(self, siblings, route_parts, method, path_params):
        part = route_parts[0]
        if part in siblings:
            if len(route_parts) > 1:
                return self.__find(siblings[part].children, route_parts[1:], method, path_params)
            else:
                if method in siblings[part].callbacks:
                    return siblings[part].callbacks.get(method), path_params
                else:
                    raise NoMethodFoundError('No {} method found on /{}'.format(method, '/'.join(route_parts)))
        
        elif helpers.path_param_exist(siblings):
            path_param = helpers.get_path_param(siblings)
            cleaned_param = helpers.clean_up_path_param(path_param)
            path_params[cleaned_param] = part
            if len(route_parts) > 1:
                return self.__find(siblings[path_param].children, route_parts[1:], method, path_params)
            else:
                if method in siblings[path_param].callbacks:
                    return siblings[path_param].callbacks.get(method), path_params
                else:
                    raise NoMethodFoundError('No method found')
        else:
            raise NoRouteFoundError('No route part found on /{}'.format('/'.join(route_parts)))

    def __str__(self):
        return str(self.root)

class Node:
    def __init__(self, value, resource_path):
        self.value = value
        self.resource_path = resource_path
        self.callbacks = {} 
        self.children = {} 

    def __str__(self):
        ret = '(value="{}" resource_path={} callbacks={} children: ['.format(self.value, self.resource_path, self.callbacks)
        ret += ', '.join(list(map(lambda n: n + ':' + str(self.children[n]), self.children.keys())))
        ret += '])'
        return ret


routing_tree = RoutingTree()
