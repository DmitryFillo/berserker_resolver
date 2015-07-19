from berserker_resolver import Resolver

def tries_detect(domain='youtube.com', cycles=100, **kwargs):
    tries = 0
    max_length = 0

    for i in range(cycles):
        while True:
            tries += 1
            r = Resolver(tries=tries, **kwargs)

            new_lengths = set()
            for i in range(cycles):
                new_lengths.add(len(r.resolve([domain])[domain]))

            if len(new_lengths) != 1:
                max_length = max(new_lengths)
                continue

            if list(new_lengths)[0] <= max_length:
                break

    return tries
