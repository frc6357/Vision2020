import itertools
from closer_0 import *
from removeDuplicates import *
input = [-0.052104208416833664, -2.0513698630136985, 1.5404411764705883, 1.5404411764705883, -0.052104208416833664, -2.0513698630136985]
slope = input
slope = [a for a in itertools.combinations(slope, 2)]
slope = [close_to_0(a) for a in slope]
slope = remov_dupl(slope)
slope = [a for a in itertools.combinations(slope, 2)]

while len(slope) > 2:
    slope = [close_to_0(a) for a in slope]
    slope = remov_dupl(slope)
    slope = [a for a in itertools.combinations(slope, 2)]
    slope = [a for t in slope for a in t]

print(slope)


