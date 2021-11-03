import math
a = [350, 10]
b = [90, 180, 270, 360]
c = [10, 20, 30]

def avgAngle(input):
    sumY = 0
    sumX = 0
    count = 0
    for i in input:
        i = i * math.pi/180
        count += 1
        sumY += math.sin(i)
        sumX += math.cos(i)
    print("count: " + str(count))
    return int((math.atan2(sumY/count, sumX/count)) * 180/math.pi)

print(avgAngle(a))
print("\n")
print(avgAngle(b))
print("\n")
print(avgAngle(c))