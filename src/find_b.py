def find_b(m, input):
    output = [a for a in input if a[0] == m]
    if len(output) > 1:
        output_b = [a[1] for a in output]
        smallest_b = max(output_b)
        output = [a for a in input if a[0] == m and a[1] == smallest_b]
        output = [a for t in output for a in t]
        return output
    else:
        output = [a for t in output for a in t]
        return output