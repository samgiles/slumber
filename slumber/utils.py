import posixpath

try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urlparse import urlsplit, urlunsplit


def url_join(base, *args):
    """
    Helper function to join an arbitrary number of url segments together.
    """
    scheme, netloc, path, query, fragment = urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[('%s' % x) for x in args])
    return urlunsplit([scheme, netloc, path, query, fragment])

def copy_kwargs(dictionary):
	kwargs = {}
	for key, value in iterator(dictionary):
		kwargs[key] = value

	return kwargs

def iterator(d):
    """
    Helper to get and a proper dict iterator with Py2k and Py3k
    """
    try:
        return d.iteritems()
    except AttributeError:
        return d.items()
