def checkParameters(callback, method_name, timeout):
    if callback is not None and not callable(callback):
        raise Exception("%s: callback is not a function" % method_name)
    if not isinstance(timeout, int):
        raise Exception("%s: timeout is not an integer" % method_name)
    if timeout < 0:
        raise Exception("%s: timeout must be greater or equal to 0" % method_name)
