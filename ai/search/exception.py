class SearchException(Exception):
    pass


class NoValidPathException(SearchException):
    pass


class DepthLimitReachedException(SearchException):
    pass


class InputException(SearchException):
    pass
