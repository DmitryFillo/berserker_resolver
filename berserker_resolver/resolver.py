# -*- coding: utf-8 -*-

from berserker_resolver.query import Query
from berserker_resolver.concurrence import ThreadConcurrence
from berserker_resolver.mixins import WwwMixin
from berserker_resolver.base import MroFix

class BaseResolver(object):
    def __init__(self, **kwargs):
        super(BaseResolver, self).__init__(**kwargs)

    def resolve(self, domains):
        resolver = self.get_resolver()
        resolved = resolver(domains)
        return resolved

class ThreadResolver(WwwMixin, BaseResolver, Query, ThreadConcurrence, MroFix):
    def __init__(self, **kwargs):
        super(ThreadResolver, self).__init__(**kwargs)

    def get_resolver(self):
        return self.thread_resolver
