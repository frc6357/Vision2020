def solve_syseq(input):
    first, second = input
    m1 = first[0]
    b1 = first[1]
    m2 = second[0]
    b2 = second[1]
    if (m1 == m2):
        return None

    else:
        x = (b2-b1)/(m1-m2)
        y = m1*x +b1
        if (x < 0):
            return None
        elif (y < 0):
            return None
        else:
            return (int(x), int(y))



