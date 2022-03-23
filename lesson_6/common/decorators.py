import sys
from inspect import stack
import time

def log(func):
    def wrap(*args, **kwargs):
        res = func(*args, **kwargs)

        ## вариант с использованием inspect
        # print("CALLER FUNCTION: {}".format(stack()[1].function))

        ## вариант с использованием sys._getframe()
        print(f'log: <{time.asctime()}> The function <{func.__name__}> is called by <{sys._getframe().f_back.f_code.co_name}>')
        print(f'log: <{time.asctime()}> {func.__name__}({args, kwargs}) = {res}')
        return res
    return wrap

