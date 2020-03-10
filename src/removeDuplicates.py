def remov_dupl_array(input):
    return [t for t in (set(tuple(i) for i in input))]

def remov_dupl(input):
    final_list = []
    for num in input:
        if num not in final_list:
            final_list.append(num)
    return final_list