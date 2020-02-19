import math
import itertools

output = []

input = ([1.4821109123434706, 135.87298747763873], [-1.9636163175303198, 918.9834619625137], [1.4843330349149508, 150.16114592658914])

slope_offset = [[1.4821109123434706, 135.87298747763873], [-1.9636163175303198, 918.9834619625137], [1.4843330349149508, 150.16114592658914], [-0.052104208416833664, 419.14629258517033], [-0.05207811717576365, 411.1196795192789], [-1.9636163175303198, 935.728776185226]]
if input in slope_offset:
    print(True, "input is in triangles")
else:
    print(False, "input is not in triangles")

triangles = [a for a in itertools.combinations(slope_offset, 3)]

first, second, third = input
m1 = first[0]
m2 = second[0]
m3 = third[0]
accept_angles = [0, 1, 2, 57, 58, 59]
theta1 = int(math.atan(m1) * 180/math.pi)
theta_01 = theta1 if theta1 <= 180 else 360-theta1

print("theta1 calculated")

theta_01 = abs(theta_01)
theta2 = int(math.atan(m2) * 180/math.pi)
theta_02 = theta2 if theta2 <= 180 else 360-theta2
print("theta2 calculated")
theta_02 = abs(theta_02)
theta3 = int(math.atan(m3) * 180/math.pi)
theta_03 = theta3 if theta3 <= 180 else 360-theta3

print("theta3 calculated")

theta_03 = abs(theta_03)
min_theta = min(theta_01, theta_02, theta_03)

print("mind found")

theta_offset = [a for a in [theta1, theta2, theta3] if abs(a) == min_theta][0]
theta1 = theta1-theta_offset
theta2 = theta2-theta_offset
theta3 = theta3-theta_offset

print("thetas are ready to be compared")

if theta1-theta2 in accept_angles:
    output = None
if theta1-theta3 in accept_angles:
    output = None
if theta2-theta3 in accept_angles:
    output = None

if (theta1 + theta2) % 60 not in accept_angles:
    output = None

if (theta1 + theta3) % 60 not in accept_angles:
    output = None


if (theta2 + theta3) % 60 not in accept_angles:
    output = None


output = (first, second, third)

print(output, "triangle found")

print(triangles)