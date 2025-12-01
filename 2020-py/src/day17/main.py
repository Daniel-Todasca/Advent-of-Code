from src.helper import IO
import itertools

CNT_ITER = 6


def get_all_neighbours(pt):
    # [adj for adj in itertools.product(range(pt[0]-1, pt[0]+2), range(pt[1]-1, pt[1]+2), range(pt[2]-1, pt[2]+2)
    return [adj for adj in itertools.product(range(pt[0]-1, pt[0]+2), range(pt[1]-1, pt[1]+2),
                                             range(pt[2]-1, pt[2]+2), range(pt[3]-1, pt[3]+2))
            if adj != pt]


def check(state_set, accumulator_set, candidate_cube):
    active_neighbours = len([x for x in get_all_neighbours(candidate_cube) if x in state_set])
    if candidate_cube in state_set and 2 <= active_neighbours <= 3:
        accumulator_set.add(candidate_cube)
    elif candidate_cube not in state_set and active_neighbours == 3:
        accumulator_set.add(candidate_cube)


file_input = IO.read_all()
# active_cubes = set([(x, y, 0) for x, line in enumerate(file_input) for y, ch in enumerate(line) if ch == '#'])
active_cubes = set([(x, y, 0, 0) for x, line in enumerate(file_input) for y, ch in enumerate(line) if ch == '#'])

for _ in range(CNT_ITER):
    next_cubes = set()
    for cube in active_cubes:
        check(active_cubes, next_cubes, cube)
        for neighbour in get_all_neighbours(cube):
            check(active_cubes, next_cubes, neighbour)
    active_cubes = next_cubes

IO.write(len(active_cubes))
