
import math

def detect_tri(input):
    first, second, third = input
    m1 = first[0]
    m2 = second[0]
    m3 = third[0]
    accept_angles = [0, 1, 2, 3, 56, 57, 58, 59]
    accept_angles_subtract = [0, 1, 2]
    theta1 = int(math.atan(m1) * 180/math.pi)
    theta_01 = theta1 if theta1 <= 180 else 360-theta1
    theta_01 = abs(theta_01)
    theta2 = int(math.atan(m2) * 180/math.pi)
    theta_02 = theta2 if theta2 <= 180 else 360-theta2
    theta_02 = abs(theta_02)
    theta3 = int(math.atan(m3) * 180/math.pi)
    theta_03 = theta3 if theta3 <= 180 else 360-theta3
    theta_03 = abs(theta_03)
    min_theta = min(theta_01, theta_02, theta_03)
    theta_offset = [a for a in [theta1, theta2, theta3] if abs(a) == min_theta][0]
    theta1 = theta1-theta_offset
    theta2 = theta2-theta_offset
    theta3 = theta3-theta_offset

    if abs(theta1-theta2) in accept_angles_subtract:
        print(theta1-theta2, "subtract")
        return None
    if abs(theta1-theta3) in accept_angles_subtract:
        print(theta1-theta3, "subtract")
        return None
    if abs(theta2-theta3) in accept_angles_subtract:
        print(theta2-theta3, "subtract")
        return None

    if (theta1 + theta2) % 60 not in accept_angles:
        print((theta1 + theta2) % 60, "modulo")
        return None

    if (theta1 + theta3) % 60 not in accept_angles:
        print((theta1 + theta3) % 60, "modulo")
        return None


    if (theta2 + theta3) % 60 not in accept_angles:
        print((theta2 + theta3) % 60, "modulo")
        return None


    return (first, second, third)




