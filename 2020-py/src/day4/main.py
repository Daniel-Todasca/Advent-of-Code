from src.helper import IO
import re


eye_colours = [
    "amb", "blu", "brn", "gry", "grn", "hzl", "oth"
]


def check_byr(value):
    if re.match(r"^\d{4}$", value):
        return 1920 <= int(value) <= 2002
    return False


def check_iyr(value):
    if re.match(r"^\d{4}$", value):
        return 2010 <= int(value) <= 2020
    return False


def check_eyr(value):
    if re.match(r"^\d{4}$", value):
        return 2020 <= int(value) <= 2030
    return False


def check_hgt(value):
    if re.match(r"^\d{3}cm$", value):
        return 150 <= int(value.split("cm")[0]) <= 193
    if re.match(r"^\d{2}in$", value):
        return 59 <= int(value.split("in")[0]) <= 76
    return False


def check_hcl(value):
    return re.match(r"^#[0-9a-f]{6}$", value)


def check_ecl(value):
    return value in eye_colours


def check_pid(value):
    return re.match(r"^\d{9}$", value)


def check_cid(value):
    return True


pass_list = []
mandatory_fields = [
    'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'
]
optional_fields = [
    'cid'
]
checkers = {
    'byr': check_byr,
    'iyr': check_iyr,
    'eyr': check_eyr,
    'hgt': check_hgt,
    'hcl': check_hcl,
    'ecl': check_ecl,
    'pid': check_pid,
    'cid': check_cid
}


def get_entries(raw_data):
    entries_dict = {}
    for pair in raw_data.split():
        arr = pair.split(":")
        entries_dict[arr[0]] = arr[1]
    return entries_dict


def parse_file():
    passport = {}
    for line in IO.read_all():
        passport.update(get_entries(line))
        if len(line) < 3 or line[-1] != '\n':
            pass_list.append(passport)
            passport = {}


def is_valid(passport):
    # for field in mandatory_fields:
    #     if field not in passport:
    #         return False
    # return True

    for field in mandatory_fields:
        if field not in passport:
            return False
        if not checkers[field](passport[field]):
            return False

    for field in optional_fields:
        if field not in passport:
            continue
        if not checkers[field](passport[field]):
            return False

    return True


parse_file()
IO.write(len([passport for passport in pass_list if is_valid(passport)]))
