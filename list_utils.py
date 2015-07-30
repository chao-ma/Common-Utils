from collections import defaultdict
"""
slice_list([1,2,3,4,5,6,7],3) -> [[1,2,3],[4,5,6],[7]]

Often, we want key -> value list map, but input is [(key, value), (key, value)...]
group_by_keys are for this purpose
group_by_keys([(1,3), (2,4), (1,5), (1,1), (3,3)]) -> {1: [3, 5, 1], 2: [4], 3: [3]}
reverse key-value order:
group_by_keys([(1,3),(2,4),(1,5),(1,1),(3,3)]) -> {1: [1], 3: [1, 3], 4: [2], 5: [1]}

Count elements in a list
count_elems([1,1,1,2,3,4,4]) -> {1: 3, 2: 1, 3: 1, 4: 2}
"""

def slice_list(input_list, length):
    ret_value = []
    for elem in input_list:
        if not ret_value or len(ret_value[-1]) == length:
            ret_value.append([])
        ret_value[-1].append(elem)
    return ret_value


def group_by_keys(key_value_list, key_id = 0, value_id = 1):
    return reduce(lambda x,y: x[y[key_id]].append(y[value_id]) or x,
                  key_value_list, defaultdict(list))


def count_elems(input_list):
    key_to_count = dict()
    for i in input_list:
        if i in key_to_count:
            key_to_count[i] += 1
        else:
            key_to_count[i] = 1
    return key_to_count
