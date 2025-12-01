from src.helper import IO
import collections

COUNT_TURNS = 2020

starting_numbers = [int(x) for x in IO.read_all()[0].split(",")]
spoken_numbers = []
number_history = collections.defaultdict(lambda: list())


def speak(x, turn):
    if len(number_history[x]) > 1:
        x = number_history[x][-1] - number_history[x][-2]
    else:
        x = 0
    spoken_numbers.append(x)
    number_history[x].append(turn)
    IO.write(turn, x)


for i in range(1, COUNT_TURNS+1):
    if i-1 < len(starting_numbers):
        spoken_numbers.append(starting_numbers[i-1])
        number_history[starting_numbers[i-1]].append(i)
    else:
        speak(spoken_numbers[-1], i)

IO.write(spoken_numbers[-1])
