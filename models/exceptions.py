class DuplicatedValue(Exception):
    def __init__(self, error_msg):
        super(DuplicatedValue, self).__init__(error_msg)


class RowNotFound(Exception):
    def __init__(self, error_msg):
        super(RowNotFound, self).__init__(error_msg)


class UnexpectedError(Exception):
    def __init__(self, error_msg):
        super(UnexpectedError, self).__init__(error_msg)