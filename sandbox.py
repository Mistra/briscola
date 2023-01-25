import functools


def wrapper(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        gne = [args[0]*2, *args[1:]]
        tmp = func(*gne, **kwargs)
        return tmp
    return inner


@wrapper
def adder(num1, num2, num3):
    return num1 + num2 + num3


res = adder(2, 2, 3)
print(res)
