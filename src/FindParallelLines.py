threshold = 10

#example output of the hough transform
numlines = 20

input = [[[415.,1.5009831 ]],

 [[76,2.5481806]],

 [[422,0.4537856]],

 [[426,1.4835298]],

 [[418,1.4835298]],

 [[423,1.5009831]],

 [[69,2.565634]],

 [[417,0.47123888]]]

print(input)
print()

angles = []
parallels = []
lonePairs = []

#extract the angles
for line in input:
    angles.append(line[0][1])


#for each angle
for i in range(0, len(angles)):
    #remember what the angle is
    angle = angles[i]
    #see how many times it appears
    angleCount = angles.count(angle)
    #if the angle is not unique
    if angleCount >= 2:
        #add the line with that angle to the parallel lines list
        parallels.append(input[i])


amountToCheck = len(parallels)

for i in range(amountToCheck):
    foundSimilar = False
    for j in range(amountToCheck):
        if parallels[i][0][1]!=parallels[j][0][1] and abs(parallels[i][0][1]-parallels[j][0][1])<=threshold:
            foundSimilar = True
    if foundSimilar:
        pass
    else:
        lonePairs.append(parallels[i])

print(lonePairs)
