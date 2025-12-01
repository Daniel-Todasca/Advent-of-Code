from src.helper import IO
import re
import numpy as np
from collections import defaultdict
import functools
import itertools


SEA_MONSTER = [
    "                  #",
    "#    ##    ##    ###",
    " #  #  #  #  #  #"
]


class Tile:
    TILE_SIZE = 10
    bd_freq = defaultdict(int)

    @staticmethod
    def bd_to_int(bd):
        return min(int(bd, 2), int(bd[::-1], 2))

    def __init__(self, tile_data):
        self.id = int(tile_data[0])
        lines = tile_data[1].replace("#", "1").replace(".", "0").split("\n")
        self._lines = np.array([[ch for ch in line] for line in lines if len(line) >= Tile.TILE_SIZE])

        for border in set(self.get_int_borders()):
            Tile.bd_freq[border] += 1

    def get_borders(self):
        return ["".join(self._lines[0]), "".join(self._lines[:, Tile.TILE_SIZE-1]),
                "".join(self._lines[Tile.TILE_SIZE-1]), "".join(self._lines[:, 0])]

    def get_int_borders(self):
        return [Tile.bd_to_int(bd) for bd in self.get_borders()]

    def get_unique_borders_count(self):
        return len([bd for bd in self.get_int_borders() if Tile.bd_freq[bd] == 1])

    def is_corner(self):
        return self.get_unique_borders_count() == 2

    def is_edge(self):
        return self.get_unique_borders_count() == 1

    def match(self, left, right, empty_right, empty_down):
        cnt = 0
        for value in [left, right]:
            if value is not None and Tile.bd_to_int(value) not in self.get_int_borders():
                return False
            if value is None:
                cnt += 1
        if empty_down: cnt += 1
        if empty_right: cnt += 1

        if cnt != self.get_unique_borders_count():
            return False

        return True

    def transform(self, code):
        if code % 3 == 0:
            self._lines = np.flipud(self._lines)
        if code % 3 == 1:
            self._lines = np.flipud(self._lines)
            self._lines = np.fliplr(self._lines)
        if code % 3 == 2:
            self._lines = np.fliplr(self._lines)
            self._lines = np.rot90(self._lines)

    def turn(self, left_str, up_str, empty_right, empty_down):
        for iteration in range(12):
            self.transform(iteration)

            int_values = self.get_int_borders()
            str_values = self.get_borders()

            if left_str is None and Tile.bd_freq[int_values[3]] != 1:
                continue
            if up_str is None and Tile.bd_freq[int_values[0]] != 1:
                continue
            if empty_right and Tile.bd_freq[int_values[1]] != 1:
                continue
            if empty_down and Tile.bd_freq[int_values[2]] != 1:
                continue
            if left_str is not None and left_str != str_values[3]:
                continue
            if up_str is not None and up_str != str_values[0]:
                continue
            break

    def str_representation(self):
        return ["".join(line).replace("1", "#").replace("0", ".") for line in self._lines]


class Grid:
    def __init__(self, tile_list):
        self.__size = int(pow(len(tile_list), 0.5))
        self.tiles = tile_list
        self.layout = dict()
        self.__build()

    def __build(self):
        self.selected_tiles = set()
        for i, j in itertools.product(range(0, self.__size), range(0, self.__size)):
            left = self.layout.get(complex(i, j-1))
            if left is not None:
                left = left.get_borders()[1]
            up = self.layout.get(complex(i-1, j))
            if up is not None:
                up = up.get_borders()[2]

            empty_right = (j == self.__size-1)
            empty_down = (i == self.__size-1)

            tile = self.get_matching_tile(left, up, empty_right, empty_down)

            if tile is None:
                print("Something's wrong, I can feel it")
            else:
                self.selected_tiles.add(tile)
                tile.turn(left, up, empty_right, empty_down)

            self.layout[complex(i, j)] = tile

    def get_matching_tile(self, left, up, empty_right, empty_down):
        for tile in self.tiles:
            if tile in self.selected_tiles:
                continue
            if tile.match(left, up, empty_right, empty_down):
                return tile
        return None

    def get_corners(self):
        return [self.layout[complex(0, 0)], self.layout[complex(0, self.__size-1)],
                self.layout[complex(self.__size-1, 0)], self.layout[complex(self.__size-1, self.__size-1)]]

    def water_size(self):
        return len([ch for line in self.get_map() for ch in line if ch == '#'])

    def get_map(self):
        ans = [[] for _ in range(self.__size * (Tile.TILE_SIZE-2))]
        for i, j in itertools.product(range(0, self.__size), range(0, self.__size)):
            str_tile = self.layout[complex(i, j)].str_representation()
            str_tile = str_tile[1:-1]
            str_tile = [line[1:-1] for line in str_tile]
            for idx, line in enumerate(str_tile):
                ans[i * (Tile.TILE_SIZE-2) + idx] += line
        return ans

    def get_monster_count(self):
        map_array = np.array([[ch for ch in line] for line in self.get_map()])
        for iteration in range(12):
            if iteration % 3 == 0:
                map_array = np.flipud(map_array)
            if iteration % 3 == 1:
                map_array = np.flipud(map_array)
                map_array = np.fliplr(map_array)
            if iteration % 3 == 2:
                map_array = np.fliplr(map_array)
                map_array = np.rot90(map_array)

            monster_count = count_monsters(["".join(line) for line in map_array])
            if monster_count != 0:
                return monster_count
        return 10000000000


def count_monsters(str_map):
    # IO.write(*["".join(line) for line in str_map], sep='\n', fin='x\nx\n')
    cnt = 0
    for i in range(len(str_map)):
        for j in range(len(str_map[i])):
            flag = True
            for x in range(len(SEA_MONSTER)):
                for y in range(len(SEA_MONSTER[x])):
                    if i+x not in range(len(str_map)):
                        flag = False
                    elif j+y not in range(len(str_map[i+x])):
                        flag = False
                    elif SEA_MONSTER[x][y] == '#' and str_map[i+x][j+y] != '#':
                        flag = False
            if flag:
                cnt += 1
    return cnt


tiles = [Tile(tile_data) for tile_data in re.findall(r"Tile (\d+):\n((?:[.#]+\n*){10})", "".join(IO.read_all()))]
IO.write(functools.reduce(lambda x, y: x*y, [tile.id for tile in tiles if tile.is_corner()]))
grid = Grid(tiles)
IO.write(functools.reduce(lambda x, y: x*y, [tile.id for tile in grid.get_corners()]))

IO.write(grid.water_size() - grid.get_monster_count() * 15)
