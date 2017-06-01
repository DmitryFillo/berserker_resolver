#!/home/fillo/venv/python3/bin/python

from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-random-domains.txt'
domains = list(set([d.decode('utf-8').replace('\n', '') for d in urlopen(url)]))[:2000]

from berserker_resolver import BerserkerResolver


def main():
    r = BerserkerResolver()
    g = r.resolve_until_complete(domains or ['fillo.ru', 'ya.ru'])
    print([(i.domain, i.merge_by_field('host'), i.merge_by_field('ttl')) for i in g.values()])

if __name__ == '__main__':
    main()
