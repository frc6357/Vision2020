#example output of the hough transform
lines = [
    [[1,19]],
    [[2,12]],
    [[3,13]],
    [[4,12]],
    [[5,15]],
    [[6,15]],
    [[7,18]],
    [[8,13]],
                ]
angles = []

linesWithParallels = []

#extract the angles
for line in lines:
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
        linesWithParallels.append(lines[i][0])

print(linesWithParallels)
