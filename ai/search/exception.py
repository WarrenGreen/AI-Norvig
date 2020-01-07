class SearchException(Exception):
    pass


class NoValidPathException(SearchException):
    pass


class DepthLimitReachedException(SearchException):
    pass


class CostLimitReachedException(SearchException):
    def __init__(self, cost, *args):
        super().__init__(*args)
        self.cost = cost


class InputException(SearchException):
    pass
