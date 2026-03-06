#!/usr/bin/env python
# Source: http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/#c1

import time
from collections import OrderedDict

class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2, maxsize=512):
        self.timeout = timeout
        self.maxsize = maxsize

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = OrderedDict()
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = OrderedDict()
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            now = time.time()
            try:
                v = self.cache[key]
                if (now - v[1]) > self.timeout:
                    raise KeyError
                self.cache.move_to_end(key)
            except KeyError:
                v = self.cache[key] = f(*args, **kwargs), now
                while len(self.cache) > self.maxsize:
                    self.cache.popitem(last=False)
            return v[0]
        func.func_name = f.__name__

        return func
