from src.helper import IO


def code_to_xy(code):
    code = code.replace('B', '1').replace('F', '0').replace('L', '0').replace('R', '1')
    return int(code[:7], 2), int(code[7:], 2)


def xy_to_id(xy):
    return xy[0]*8 + xy[1]


input_data = IO.read_all()
# IO.write(max([xy_to_id(code_to_xy(line.strip())) for line in input_data if len(line) > 2]))
ids = [xy_to_id(code_to_xy(line.strip())) for line in input_data if len(line) > 2]
ids_set = set(ids)

for seat_id in ids:
    if seat_id - 2 in ids_set and seat_id - 1 not in ids_set:
        IO.write(seat_id-1)
