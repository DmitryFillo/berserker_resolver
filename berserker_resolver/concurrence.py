# -*- coding: utf-8 -*-

from berserker_resolver.base import set_kwargs, get_version, xrange_compat

_version = get_version()

from threading import Thread

if _version == 3:
    from queue import Queue, Empty
elif _version == 2:
    from Queue import Queue, Empty

from math import ceil

class BaseConcurrence(object):
    threads = 8

    def __init__(self, **kwargs):
        set_kwargs(self, kwargs, ['threads'])
        super(BaseConcurrence, self).__init__(**kwargs)

    def chunk_domains(self, domains):
        domains_one_thread = int(ceil(float(len(domains))/self.threads))
        return self._chunk_list(domains, domains_one_thread)

    def _chunk_list(self, l, n):
        for i in xrange_compat(0, len(l), n):
            yield l[i:i+n]

class ThreadConcurrence(BaseConcurrence):
    queue = Queue()

    def __init__(self, **kwargs):
        super(ThreadConcurrence, self).__init__(**kwargs)

    def thread_resolver(self, domains):
        chunks = self.chunk_domains(domains)
        threads = []
        for i in xrange_compat(self.threads):
            try:
                chunk = next(chunks)
            except StopIteration:
                break
            t = Thread(target=self.__thread, args=(chunk,))
            t.start()
            threads.append(t)
        [t.join() for t in threads]
        result = []
        while True:
            try:
                result.append(self.queue.get(block=False))
            except Empty:
                break
        return result

    def __thread(self, domains):
        for d in domains:
            self.queue.put((d, self.query(d)))

    def query(self, domain):
        return NotImplementedError('query method is function for query one domain, implement it')
