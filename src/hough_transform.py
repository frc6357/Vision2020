def threshold(x, rho_theta):
    rho, theta = rho_theta
    rho_1, theta_1 = x
    if (abs(rho-rho_1) < 0.05*rho) and (abs(theta-theta_1) < 0.05*theta):
        return True
    else:
        return False


def filter_lines(lines, bucket):
    next_set_to_process = []

    # initial rho and theta in the total list of lines
    matching_set = [lines[0]]
    rho, theta = lines[0]

    # iterating through all the other rhos and thetas excluding the first
    for x in lines[1:]:
        # if lines meet threshold condition (within 5% of the original rho and theta) then add to the matching set
        if threshold(x, lines[0]):
            matching_set.append(x)
        else:
            # if lines are outside 5% of the original rho and theta then add to the next set
            next_set_to_process.append(x)
    bucket.append(matching_set)
    return next_set_to_process, bucket


def average_lines(lines):
    avg_lines = []
    for dupl_lines in lines:
        length = len(lines)
        sum_rho = 0
        sum_theta = 0
        for i in dupl_lines:
            sum_rho += i[0]
            sum_theta += i[1]
        avg_rho = sum_rho/length
        avg_theta = sum_theta/length
        avg_lines.append([avg_rho, avg_theta])
    return avg_lines

