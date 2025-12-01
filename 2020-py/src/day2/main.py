from src.helper import IO
import re


valid_pass_count = 0
for line in IO.read_all():
    match = re.match(r"(\d*-\d*)\s*(\w):\s*(\w+)", line)
    if match is None:
        continue

    bounds = [int(x) for x in match.group(1).split('-')]
    character = match.group(2)
    word = match.group(3)
    count = word.count(character)

    # if bounds[0] <= count <= bounds[1]:
    #     valid_pass_count += 1

    if [word[bounds[0]-1], word[bounds[1]-1]].count(character) == 1:
        valid_pass_count += 1

IO.write(valid_pass_count)
