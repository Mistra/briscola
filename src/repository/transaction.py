import functools

from flask import g

# def transactional(func):
#     wraps(func)

#     def call_func(*args, **kwargs):
#         self = args[0]
#         g.get("transaction_nesting")
#         if "transaction_nesting" in g:
#             g.transaction_nesting += 1
#         else:
#             g.transaction_nesting = 1
#             g.current_cursor = self.connection.cursor()
#         # print(f"Called {func.__name__} with level {g.get('transaction_nesting')}")
#         tmp = func(*args, **kwargs, cursor=g.current_cursor)
#         g.transaction_nesting -= 1
#         if g.transaction_nesting == 0:
#             self.connection.commit()
#             g.pop('current_cursor').close()
#             g.pop('transaction_nesting')
#         return tmp
#     return call_func


def transaction(flask_g, db_conn):
    def inner_wrapper(func):
        @functools.wraps(func)
        def call_func(*args, **kwargs):
            self = args[0]
            flask_g.get("nesting_counter")
            if "nesting_counter" in g:
                flask_g.nesting_counter += 1
            else:
                flask_g.nesting_counter = 1
                flask_g.current_cursor = self.connection.cursor()
            tmp = func(*args, **kwargs, cursor=g.current_cursor)
            flask_g.nesting_counter -= 1
            if flask_g.nesting_counter == 0:
                self.connection.commit()
                flask_g.pop('current_cursor').close()
                flask_g.pop('nesting_counter')
            return tmp
        return call_func
    return inner_wrapper
