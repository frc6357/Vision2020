import itertools
from closer_0 import *
from removeDuplicates import *
def approx_0_slope(input):
    slope = input
    slope = [a[0] for a in slope]
    slope = [a for a in itertools.combinations(slope, 2)]
    slope = [close_to_0(a) for a in slope]
    slope = remov_dupl(slope)
    slope = [a for a in itertools.combinations(slope, 2)]
    #print(len(slope), "slope length")
    slope_length = len(slope)
    while slope_length > 1:
      #  print("beginning of while loop:", slope)

        slope = [close_to_0(a) for a in slope]
        slope = remov_dupl(slope)
        slope_length = len(slope)
       # print("filtering:", slope)
        if slope_length == 1:
            #print("slope of length 1:")
            #print(slope)
            return slope
        slope = [a for a in itertools.combinations(slope, 2)]
        #print("recombining:", slope)
        slope = remov_dupl(slope)
        #print("bottom of while loop:", slope)
        #print(slope_length, "slope length in loop")




