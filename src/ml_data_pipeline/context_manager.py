from contextlib import contextmanager


@contextmanager
def managed_resource(resource):
    try:
        yield resource
    finally:
        resource.close()
