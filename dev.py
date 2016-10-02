from berserker_resolver import Resolver

def main():
    r = Resolver(www=True)
    g = r.resolve_until_complete(['fillo.me', 'www.ya.ru'])
    print(g)

if __name__ == '__main__':
    main()
