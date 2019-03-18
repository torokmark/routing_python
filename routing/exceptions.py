
class NoMethodFoundError(Exception):
    def __init__(self, message):
        self.message = message

class NoRouteFoundError(Exception):
    def __init__(self, message):
        self.message = message

class RouteNotValidError(Exception):
    def __init__(self, message='Route is not valid.'):
        self.message = message

class QueryNotValidError(Exception):
    def __init__(self, message='Query is not valid'):
        self.message = message

