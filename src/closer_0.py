def close_to_0(input):
    f = input[0]
    s = input[1]
    if abs(f) < abs(s):
        return f
    else:
        return s