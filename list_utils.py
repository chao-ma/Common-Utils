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

insert_pos: my implementation of bisect_right, find the right most position to insert
            an element into a sorted list and maintain the sorted order
histogram: given a list of samples and bins, count elements in each bin
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


def insert_pos(input_list, elem):
    """
    input_list is a sorted list of elements comparable to elem.
    It finds a position i where input_list[i - 1] <= elem < input_list[i]
    """
    begin = 0
    end = len(input_list) - 1
    while begin <= end:
        mid = (begin + end) // 2
        if input_list[mid] <= elem:
            begin = mid + 1
        else:
            end = mid - 1
    return begin

def histogram(input_list, bins):
    """
    create len(bins) + 1 list
    e.g. bins = [1,3,5,7], it will create interval [-infi, 1) [1,3), [3,5), [5,7), [7,infi)
    and count how many elems in input_list fall into the bins
    bins need to be sorted
    """
    hist = [0] * (len(bins) + 1)
    for elem in input_list:
        pos = insert_pos(bins, elem)
        hist[pos] += 1
    return hist
