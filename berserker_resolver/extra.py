from berserker_resolver import Resolver

def detect_tries(domain='youtube.com', cycles=100, **kwargs):
    tries_all = []

    for i in range(cycles):
        tries = 0
        k = 0

        while True:
            if k == 0:
                tries += 1

            r = Resolver(tries=tries, **kwargs)

            new_lengths = set()
            for i in range(cycles):
                new_lengths.add(len(r.resolve([domain])[domain]))

            if len(new_lengths) != 1:
                k = 0
                continue

            k += 1

            if k >= cycles:
                break

        tries_all.append(tries)

    return max(tries_all)
