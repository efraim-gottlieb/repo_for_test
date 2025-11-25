import sqlite3
from functools import wraps

def session(func):
    @wraps(func)
    def inner(url, *args, **kwargs):
        cnx = sqlite3.connect(url)
        cnx.row_factory = sqlite3.Row
        cursor = cnx.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            if cnx.in_transaction:
                cnx.commit()
            return result
        except Exception as err:
            cnx.rollback()
            print(f'err: {err}')
            raise
        finally:
            cursor.close()
            cnx.close()
    return inner

