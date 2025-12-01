from src.helper import IO
import itertools


cache = {}


def parse_rule(rule_string):
    idx, definition = rule_string.split(":")
    possibilities = definition.strip().replace("\"", "")
    if definition.find("\"") == -1:
        possibilities = [[int(x) for x in possibility.split()] for possibility in definition.split("|")]
    return int(idx), possibilities


def build_cache(rule):
    if rule in cache:
        return
    if isinstance(rules[rule], str):
        cache[rule] = [rules[rule]]
    else:
        cache[rule] = []
        for possibility in rules[rule]:
            for dependency in possibility:
                build_cache(dependency)
            cache[rule].extend(["".join(subrules) for subrules in itertools.product(*[cache[x] for x in possibility])])


def match(rule, message):
    build_cache(rule)
    return message in cache[rule]


def match_rep(message, rule):
    for var in cache[rule]:
        if var == message:
            return True
        if var == message[:len(var)]:
            if match_rep(message[len(var):], rule):
                return True


def match_11(message, sgn=0):
    if sgn == 0:
        for var in cache[42]:
            if var != message and var == message[:len(var)]:
                if match_11(message[len(var):], 1):
                    return True
    else:
        for var in cache[31]:
            if var == message:
                return True
            if len(var) <= len(message) and var == message[-len(var):]:
                if match_11(message[:-len(var)], 0):
                    return True
    return False


def match_8_11(message):
    for i in range(len(message)):
        if match_rep(message[:i], 8) and match_11(message[i:]):
            return True
    return False


file_input = IO.read_all()
index = file_input.index("\n")
rules, messages = file_input[:index], file_input[(index+1):]
rules = dict(parse_rule(rule) for rule in rules)

build_cache(8)
build_cache(11)

IO.write(len([message for message in messages if match(0, message.strip())]))
IO.write(len([message for message in messages if match_8_11(message.strip())]))
