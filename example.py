# -*- coding: utf-8 -*-

from berserker_resolver import ThreadResolver

domains = ['yandex.ru', 'google.com']

resolver = ThreadResolver()
resolved = resolver.resolve(domains)

print(resolved)
