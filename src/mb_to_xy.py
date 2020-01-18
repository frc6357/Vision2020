from src.systemeq import *
def mb_xy(input):
    f, s, t = input
    f1 = solve_syseq((f,s))
    s1 = solve_syseq((f,t))
    t1 = solve_syseq((s,t))

    return (f1, s1, t1)



