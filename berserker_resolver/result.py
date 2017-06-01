class BerserkerResult(object):
    def __init__(self, domain, result=None):
        self._domain = domain
        if result:
            self._result = set(result)
        else:
            self._result = set()

    @property
    def domain(self):
        return self._domain

    @property
    def result(self):
        return self._result

    def merge_by_field(self, prop):
        r = set()
        for i in self._result:
            r.add(getattr(i, prop))
        return r

    def __str__(self):
        return self._domain

    def __add__(self, other):
        if other.domain != self._domain:
            raise TypeError('You can add BerserkerResult instance to another only if domains are equal.')
        return BerserkerResult(domain=self._domain, result=self._result.union(other.result))
