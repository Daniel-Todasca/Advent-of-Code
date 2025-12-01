from src.helper import IO
import functools

tree_map = [line.strip() for line in IO.read_all()]


# vel, grid_pos = complex(3, 1), complex(0, 0)
# tree_counter = 0
grid_height, grid_width = len(tree_map), len(tree_map[0])


def is_tree(x, y):
    return tree_map[y][x % grid_width] == '#'


def get_coord(complex_num):
    return int(complex_num.real), int(complex_num.imag)


def walk(velocity):
    grid_pos = complex(0, 0)
    tree_counter = 0
    while grid_pos.imag < grid_height:
        if is_tree(*get_coord(grid_pos)):
            tree_counter += 1
        grid_pos += velocity
    return tree_counter


# while grid_pos.imag < grid_height:
#     if is_tree(*get_coord(grid_pos)):
#         tree_counter += 1
#     grid_pos += vel


slopes = [
    complex(1, 1), complex(3, 1), complex(5, 1),
    complex(7, 1), complex(1, 2)
]
IO.write(functools.reduce(lambda x, y: x*y, [walk(slope) for slope in slopes]))
