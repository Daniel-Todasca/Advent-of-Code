from src.helper import IO
import re
import numpy as np


def parse_rule(rule_str):
    match = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", rule_str)
    return match.group(1), ((int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5))))


def is_valid(value):
    return len(list(filter(lambda x: x[0][0] <= value <= x[0][1] or x[1][0] <= value <= x[1][1], rules.values()))) > 0


def are_valid_values(values, r):
    return len(list(filter(lambda x: r[0][0] <= x <= r[0][1] or r[1][0] <= x <= r[1][1], values))) == len(values)


def is_valid_ticket(ticket):
    return len(list(filter(lambda value: not is_valid(value), ticket))) == 0


ticket_index, nearby_index = IO.read_all().index("your ticket:\n"), IO.read_all().index("nearby tickets:\n")
rules = dict(parse_rule(rule_line) for rule_line in IO.read_all()[:ticket_index-1])
self_ticket = [int(x) for x in IO.read_all()[ticket_index+1].split(',')]
nearby_tickets = [[int(x) for x in line.split(',')] for line in IO.read_all()[nearby_index+1:]]

IO.write(sum([value for ticket in nearby_tickets for value in ticket if not is_valid(value)]))


nearby_tickets = list(filter(lambda ticket: is_valid_ticket(ticket), nearby_tickets))
matrix = np.array([self_ticket] + nearby_tickets)

product = 1
while len(rules) > 0:
    to_remove = []

    for name, rule in rules.items():
        valid_columns = [i for i in range(len(matrix[0])) if are_valid_values(matrix[:, i], rule)]

        if len(valid_columns) == 1:
            if "departure" in name:
                product *= int(matrix[0][valid_columns[0]])

            to_remove.append(name)
            matrix = np.delete(matrix, valid_columns[0], 1)

    for task in to_remove:
        rules.pop(task)

IO.write(product)
