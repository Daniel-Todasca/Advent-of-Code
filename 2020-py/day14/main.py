from src.helper import IO
import re
import itertools


def powerset(iterable):
    return itertools.chain.from_iterable(itertools.combinations(iterable, index) for index in range(len(iterable) + 1))


mask_one, mask_zero, float_values = None, None, None
memory = dict()
for line in IO.read_all():
    match_mask = re.match(r"mask = ([10X]{36})", line)
    match_memo = re.match(r"mem\[(\d+)] = (\d+)", line)

    if match_mask:
        mask = [(index, int(bit) if bit != "X" else bit) for index, bit in enumerate(match_mask.group(1))]
        mask_one = sum([(1 << (35-index)) for index, bit in mask if bit == 1 or bit == "X"])
        # mask_zero = ((1 << 36) - 1) ^ sum([(1 << (35-index)) for index, bit in mask if bit == 0])
        float_values = [(1 << (35-index)) for index, bit in mask if bit == "X"]
    if match_memo:
        # memory[int(match_memo.group(1))] = mask_one | int(match_memo.group(2)) & mask_zero
        for subset in powerset(float_values):
            mask_zero = (2 << 36) - 1 - sum(subset)
            memory[(mask_one | int(match_memo.group(1))) & mask_zero] = int(match_memo.group(2))


IO.write(sum(memory.values()))
