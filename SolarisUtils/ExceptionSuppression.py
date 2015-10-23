__author__ = 'Piotr Goryl'

from threading import Lock


class ExceptionSuppresser:
    '''
    Tool class that provides a functionality of suppression of exceptions for certanin number of throwing and let reapeat
    a function few times.
    '''
    global_lock = Lock()
    global_counter = 0

    def __init__(self):
        self.local_counter = 0
        self.local_lock = Lock()

    def reset_counter(self):
        '''
        Reset (set to 0) the local (object) counter of exceptions
        :return:
        '''
        with self.local_lock: # we made it thread safe
            self.local_counter = 0

    def suppress_exceptions(self,_limit, _func,_args, _exceptions_included=(Exception,), _global_limit = 0):
        """
        Run a specified function and repeat it up to _limit in case of exception. If the _limit number is crossed
        exception is raised. It checks for a local object counter and if _global_limit > 0 for global exception counter,

        :param _limit: suppress exceptions from _exceptions_included list (repeat _func(*_args) in case of an exception
        raised ) until a local (object) exception counter is less or equal this value
        :param _func: function to call
        :param _args: arguments to be passed to _func
        :param _exceptions_included: touple of exception classes to be suppressed
        :param _global_limit: suppress the exception until the global exception counter is less or equal this value and
        include it in the counter
        :return: return value of _func(*_args) or exception
        """
        while True:
            try:
                return _func(*_args)
            except _exceptions_included:
                with self.local_lock:
                    self.local_counter+=1
                    if self.local_counter > _limit:
                        raise
                if _global_limit>0:
                    with ExceptionSuppresser.global_lock:
                        ExceptionSuppresser.global_counter+=1
                        if ExceptionSuppresser.global_counter > _global_limit:
                            raise




def reset_global_counter():
    '''
    Static method.
    Reset (set to 0) the global counter of exceptions
    :return:
    '''
    with ExceptionSuppresser.global_lock: # we made it thread safe
        ExceptionSuppresser.global_counter = 0


def suppress_exceptions(_limit,_func,_args, _exceptions_included=(Exception,), _global_limit = 0):
    """
    Run a specified function and repeat it up to _limit in case of exception. If the _limit number is crossed
    exception is raised. It can also check for global error counter if _global_limit > 0

    :param _limit: suppress exceptions from _exceptions_included list (repeat _func(*_args) in case of an exception
    raised ) until exception counter is less or equal this value
    :param _func: function to call
    :param _args: arguments to be passed to _func
    :param _exceptions_included: touple of exception classes to be suppressed
    :param _global_limit: suppress the exception until the global exception counter is less or equal this value and
    include it in the counter
    :return: return value of _func(*_args) or exception
    """
    error_counter = 0
    while True:
        try:
            return _func(*_args)
        except _exceptions_included:
            error_counter += 1
            if error_counter > _limit:
                raise
            with ExceptionSuppresser.global_lock:
                if _global_limit>0:
                    ExceptionSuppresser.global_counter+=1
                    if ExceptionSuppresser.global_counter > _global_limit:
                        raise