CACHE = {}


def cache(func):
    def wrapper(*args):
        key = '{}_{}'.format(
            func.__name__,
            '-'.join(args)
        )
        value = CACHE.get(key) or func(*args)
        CACHE[key] = value
        return value

    return wrapper
