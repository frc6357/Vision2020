threshold = 0.1

#example output of the hough transform

input = [[[415.,1.5009831 ]],

 [[76,2.5481806]],

 [[422,0.4537856]],

 [[426,1.4835298]],

 [[418,1.4835298]],

 [[423,1.5009831]],

 [[69,2.565634]],

 [[417,0.47123888]]]

#print(input)
#print()

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

#print(parallels)

i=0
#check every elelment up to the second-to-last
while i < len(parallels)-1:
    #innocent until proven guilty
    foundSimilar = False
    #store the index of the value we are comparing
    identicals = []
    identicals.append(i)
    #check it against every element after it
    for j in range(i+1,len(parallels)):
        if parallels[i][0][1] == parallels[j][0][1]:
            #store the index of the line if its parallel
            identicals.append(j)
        #otherwise, check if it is too nearby
        elif abs(parallels[i][0][1]-parallels[j][0][1]) <= threshold:
            foundSimilar = True
    if foundSimilar:
        identicals.sort(reverse = True)
        #remove the line and all its parallels if a similar one was found
        for k in identicals:
            parallels.pop(k)     
        j = j+1
    i = i+1

print(parallels)
