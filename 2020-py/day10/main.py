from src.helper import IO


input_nums = [int(x) for x in IO.read_all() if len(x) > 0]
input_nums.append(0)
input_nums.append(max(input_nums) + 3)
input_nums = sorted(input_nums)

pair_diff = [y-x for x, y in zip(input_nums, input_nums[1:])]
IO.write(pair_diff.count(1) * pair_diff.count(3))

possibilities = {0: 1}
for value in input_nums[1:]:
    possibilities[value] = possibilities.get(value-1, 0) + possibilities.get(value-2, 0) + possibilities.get(value-3, 0)
IO.write(possibilities[max(input_nums)])
