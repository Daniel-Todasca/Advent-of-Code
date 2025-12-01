from src.helper import IO


def init_group_set():
    # return set()
    return set([chr(ascii_code) for ascii_code in range(ord('a'), ord('z')+1)])


groups = []
group = init_group_set()

for line in IO.read_all():
    line_ch = [ch for ch in line if 'a' <= ch <= 'z']

    # group.update(line_ch)
    if len(line) > 0 and 'a' <= line[0] <= 'z':
        group = set([ch for ch in group if ch in line_ch])

    if len(line) < 2 or line[-1] != '\n':
        if len(group) > 0:
            groups.append(group)
        group = init_group_set()

IO.write(sum([len(x) for x in groups]))
