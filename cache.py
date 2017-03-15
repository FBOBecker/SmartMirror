from werkzeug.contrib.cache import FileSystemCache


cache = FileSystemCache('.cache', threshold=10, default_timeout=6000)


def get_cache_entry(key):
    """
    returns cache[key] or None
    """
    value = cache.get(key)
    return value


def set_cache_entry(key, value):
    """
    Add a new key/value to the cache (overwrites value, if key already exists in the cache
    """
    cache.set(key, value)