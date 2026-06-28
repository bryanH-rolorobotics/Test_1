def get_value(flag):
    if not isinstance(flag, bool):
        raise TypeError("Parameter must be a boolean")
    return 42 if flag else 21
