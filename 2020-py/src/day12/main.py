from src.helper import IO


class Ferry:
    dir_map = {"N": complex(0, 1), "E": complex(1, 0), "S": complex(0, -1), "W": complex(-1, 0)}

    def __init__(self):
        self.pos = complex(0, 0)
        self.ferry_direction = Ferry.dir_map["E"]

    def move_dir(self, direction, value):
        self.pos += direction * value

    def move_forward(self, value):
        self.move_dir(self.ferry_direction, value)

    def turn(self, value):
        dir_list = list(Ferry.dir_map.values())
        idx = dir_list.index(self.ferry_direction)
        idx = (idx + value // 90) % 4
        self.ferry_direction = dir_list[idx]


class WaypointFerry(Ferry):
    def __init__(self):
        super().__init__()
        self.waypoint = complex(10, 1)
        del self.ferry_direction

    def move_dir(self, direction, value):
        self.waypoint += direction * value

    def move_forward(self, value):
        self.pos += self.waypoint * value

    def turn(self, value):
        dir_list = list(Ferry.dir_map.values())
        self.waypoint = self.waypoint * dir_list[(1 + value // 90) % 4]


def parse_instruction(to_parse):
    instr, instr_args = to_parse[0], [int(to_parse[1:])]
    if instr in Ferry.dir_map:
        instr_args = [Ferry.dir_map[instr]] + instr_args
    if instr == "L":
        instr_args[-1] = -instr_args[-1]
    return instr, instr_args


ferry = WaypointFerry()
ferry_instr = {
    "N": ferry.move_dir, "E": ferry.move_dir, "S": ferry.move_dir, "W": ferry.move_dir,
    "L": ferry.turn, "R": ferry.turn, "F": ferry.move_forward
}
lines = IO.read_all()

for line in lines:
    if len(line) < 2:
        continue
    instruction, args = parse_instruction(line)
    ferry_instr[instruction](*args)


IO.write(int(abs(ferry.pos.real) + abs(ferry.pos.imag)))
