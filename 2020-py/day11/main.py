from src.helper import IO
import itertools
import copy


seats = [[x for x in line.strip()] for line in IO.read_all()]
n, m = len(seats), len(seats[0])


def seat_trace(pos_x, pos_y, vel_x, vel_y):
    if vel_x == 0 and vel_y == 0:
        return seats[pos_x][pos_y]

    pos_x += vel_x
    pos_y += vel_y
    while pos_x in range(n) and pos_y in range(m):
        if seats[pos_x][pos_y] != '.':
            return seats[pos_x][pos_y]
        pos_x += vel_x
        pos_y += vel_y
    return '.'


n_iter = 0
while True:
    next_seats = copy.deepcopy(seats)
    for line, coll in itertools.product(range(n), range(m)):
        # adj_seats = [seats[i][j] for i in range(max(0, line-1), min(n, line+2))
        #              for j in range(max(0, coll-1), min(m, coll+2))]
        adj_seats = [seat_trace(line, coll, i, j) for i in range(-1, 2) for j in range(-1, 2)]
        occup_cnt = adj_seats.count('#')

        if seats[line][coll] == 'L' and occup_cnt == 0:
            next_seats[line][coll] = '#'
        # if seats[line][coll] == '#' and occup_cnt >= 5:
        if seats[line][coll] == '#' and occup_cnt >= 6:
            next_seats[line][coll] = 'L'

    if next_seats == seats:
        break
    n_iter += 1
    seats = next_seats


IO.write(sum([line.count('#') for line in seats]))
IO.write(n_iter)
IO.write("\n".join(["".join([ch for ch in line]) for line in seats]))
