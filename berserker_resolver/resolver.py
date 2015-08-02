import re
import threading
from berserker_resolver.utils import locked_iterator
from berserker_resolver.query import Query


class BaseResolver(object):
    def __init__(self, *args, **kwargs):
        self.tries = kwargs.get('tries', 1)
        self.nameservers = kwargs.get('nameservers', ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])
        self.verbose = kwargs.get('verbose', False)
        self.www = kwargs.get('www', False)
        self.www_combine = kwargs.get('www_combine', False)

    def resolve(self, domains):
        domains = self._bind(domains)
        resolved = self._run_queries(domains)
        result, result_exception = self._fold(resolved)

        if self.verbose:
            return {
                'success' : result,
                'error' : result_exception,
            }
        else:
            return result

    def _bind(self, domains):
        r = re.compile(r'(?:www\.){1}(.+\..+)', re.I)
        for d in domains:
            for t in range(self.tries):
                for n in self.nameservers:
                    if self.www:
                        m = r.match(d)
                        if not m:
                            for i in (d, 'www.'+d):
                                yield i, n
                        else:
                            for i in (d, m.group(1)):
                                yield i, n
                    else:
                        yield d, n

    def _fold(self, resolved):
        r = re.compile(r'(?:www\.)?(.+\..+)', re.I)
        result = {}
        result_exception = {}
        for domain, ns, answer in resolved:
            if self.www_combine:
                domain = r.match(domain).group(1)
            if not isinstance(answer, Exception):
                result.setdefault(domain, set()).update(iter(answer))
            elif self.verbose:
                result_exception.setdefault(domain, dict()).update({ns: answer})
        return result, result_exception

    def _run_queries(self, domains):
        return NotImplemented


class Resolver(BaseResolver):
    def __init__(self, *args, **kwargs):
        super(Resolver, self).__init__(*args, **kwargs)
        self.query = Query(*args, **kwargs)

        self.threads = kwargs.get('threads', 16)
        self._lock = threading.Lock()

    @locked_iterator
    def _bind(self, *args, **kwargs):
        return super(Resolver, self)._bind(*args, **kwargs)

    def _worker(self, domains, resolved):
        for i in domains:
            answer = self.query(*i)
            with self._lock:
                resolved.append(answer)

    def _run_queries(self, domains):
        resolved = []
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self._worker, args=(domains, resolved))
            t.start()
            threads.append(t)
        for i in threads:
            i.join()
        return resolved

