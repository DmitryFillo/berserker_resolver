#!/home/fillo/venv/python3/bin/python

from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-random-domains.txt'
domains = list(set([d.decode('utf-8').replace('\n', '') for d in urlopen(url)]))[:1000]

from berserker_resolver import BerserkerResolver

def main():
    r = BerserkerResolver(tries=10, qname='A')
    g = r.resolve_until_complete(['fillo.ru'])
    print([(i.domain, i.results_merged_by_prop('ttl'), i.results) for i in g.values()])

if __name__ == '__main__':
    main()
