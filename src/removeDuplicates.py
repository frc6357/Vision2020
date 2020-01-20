def remov_dupl(input):
    return [t for t in (set(tuple(i) for i in input))]