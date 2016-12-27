def combinations(string, position=0):
    if position == len(string):
        yield []
    for comb in combinations(string, position + 1):
        yield comb
        yield comb + [string[position]]


def permutations(string):
    if len(string) == 0:
        yield ''
    else:
        for idx, char in enumerate(string):
            for perm in permutations(string[:idx] + string[idx+1:]):
                yield char + perm


def combinations(string, position=0):
    if len(string) == position:
        yield []
    else:
        for comb in combinations(string, position + 1):
            yield comb
            yield comb + [string[position]]
