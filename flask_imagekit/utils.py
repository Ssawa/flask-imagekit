import re
import random, string

# TODO - Does SimpleCache suffice?
from werkzeug.contrib.cache import SimpleCache
from hashlib import md5
from .exceptions import ImproperlyConfigured
from importlib import import_module
from tempfile import NamedTemporaryFile
from django_ported.files import File
from pilkit.utils import *

bad_memcached_key_chars = re.compile('[\u0000-\u001f\\s]+')


flask_app = None

def get_flask_app():
    return flask_app

def set_flask_app(app):
    global flask_app
    flask_app = app

def get_nonabstract_descendants(model):
    """ Returns all non-abstract descendants of the model. """
    if not model._meta.abstract:
        yield model
    for s in model.__subclasses__():
        for m in get_nonabstract_descendants(s):
            yield m


def get_by_qname(path, desc):
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a %s module." % (path, desc))
    module, objname = path[:dot], path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing %s module %s: "%s"' %
                (desc, module, e))
    try:
        obj = getattr(mod, objname)
        return obj
    except AttributeError:
        raise ImproperlyConfigured('%s module "%s" does not define "%s"'
                % (desc[0].upper() + desc[1:], module, objname))


_singletons = {}


def get_singleton(class_path, desc):
    global _singletons
    cls = get_by_qname(class_path, desc)
    instance = _singletons.get(cls)
    if not instance:
        instance = _singletons[cls] = cls()
    return instance


def get_conf():
    from .conf import Conf
    global _singletons
    instance = _singletons.get(Conf)
    if not instance:
        instance = _singletons[Conf] = Conf()
    return instance


conf = get_conf()

# TODO: Not functionally required but should find a non django way to port
def autodiscover():
    pass


def generate(generator):
    """
    Calls the ``generate()`` method of a generator instance, and then wraps the
    result in a Django File object so Django knows how to save it.

    """
    content = generator.generate()

    # If the file doesn't have a name, Django will raise an Exception while
    # trying to save it, so we create a named temporary file.
    if not getattr(content, 'name', None):
        f = NamedTemporaryFile()
        f.write(content.read())
        f.seek(0)
        content = f

    return File(content)


def call_strategy_method(file, method_name):
    strategy = getattr(file, 'cachefile_strategy', None)
    fn = getattr(strategy, method_name, None)
    if fn is not None:
        fn(file)


def sanitize_cache_key(key):
    if conf.IMAGEKIT_USE_MEMCACHED_SAFE_CACHE_KEY:
        # Memcached keys can't contain whitespace or control characters.
        new_key = bad_memcached_key_chars.sub('', key)

        # The also can't be > 250 chars long. Since we don't know what the
        # user's cache ``KEY_FUNCTION`` setting is like, we'll limit it to 200.
        if len(new_key) >= 200:
            new_key = '%s:%s' % (new_key[:200-33], md5(key).hexdigest())

        key = new_key
    return key


get_cache = SimpleCache()