class DuplicatedValue(Exception):
    def __init__(self, error_msg):
        super(DuplicatedValue, self).__init__(error_msg)
