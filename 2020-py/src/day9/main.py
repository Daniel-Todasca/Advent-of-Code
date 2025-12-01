from src.helper import IO


def is_sum_of_pair(candidate, nums):
    return candidate in [nums[i] + nums[j] for i in range(len(nums)) for j in range(len(nums)) if i != j]


def find_impostor(num_arr, preamble):
    for index in range(preamble, len(num_arr)):
        if not is_sum_of_pair(num_arr[index], num_arr[index-preamble:index]):
            return num_arr[index]
    return -1


# IO.write(find_impostor([int(x) for x in IO.read_all() if len(x) > 0], 25))
input_nums = [int(x) for x in IO.read_all() if len(x) > 0]
impostor = find_impostor(input_nums, 25)

partial_sums = [0]
for x in input_nums:
    partial_sums.append(partial_sums[-1] + x)
partial_set = set(partial_sums)

left = right = 0
for p_sum in partial_sums:
    partial_set.remove(p_sum)
    to_search = impostor + p_sum
    if to_search in partial_set:
        left = p_sum
        right = to_search
        break

IO.write(left, right, right-left, impostor)
index1 = partial_sums.index(left)
index2 = partial_sums.index(right)
IO.write(max(input_nums[index1:index2]) + min(input_nums[index1:index2]))
