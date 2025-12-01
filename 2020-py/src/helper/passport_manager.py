import re


class PassportChecker:
    eye_colours = [
        "amb", "blu", "brn", "gry", "grn", "hzl", "oth"
    ]

    @staticmethod
    def check_byr(value):
        if re.match(r"^\d{4}$", value):
            return 1920 <= int(value) <= 2002
        return False

    @staticmethod
    def check_iyr(value):
        if re.match(r"^\d{4}$", value):
            return 2010 <= int(value) <= 2020
        return False

    @staticmethod
    def check_eyr(value):
        if re.match(r"^\d{4}$", value):
            return 2020 <= int(value) <= 2030
        return False

    @staticmethod
    def check_hgt(value):
        if re.match(r"^\d{3}cm$", value):
            return 150 <= int(value.split("cm")[0]) <= 193
        if re.match(r"^\d{2}in$", value):
            return 59 <= int(value.split("in")[0]) <= 76
        return False

    @staticmethod
    def check_hcl(value):
        return re.match(r"^#[0-9a-f]{6}$", value)

    @staticmethod
    def check_ecl(value):
        return value in PassportChecker.eye_colours

    @staticmethod
    def check_pid(value):
        return re.match(r"^\d{9}$", value)

    @staticmethod
    def check_cid(value):
        return True


class PassportManager:
    mandatory_fields = [
        'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'
    ]
    optional_fields = [
        'cid'
    ]
    checkers = {
        'byr': PassportChecker.check_byr,
        'iyr': PassportChecker.check_iyr,
        'eyr': PassportChecker.check_eyr,
        'hgt': PassportChecker.check_hgt,
        'hcl': PassportChecker.check_hcl,
        'ecl': PassportChecker.check_ecl,
        'pid': PassportChecker.check_pid,
        'cid': PassportChecker.check_cid
    }

    def __init__(self):
        self.pass_list = []

    def parse_lines(self, lines):
        passport = {}
        for line in lines:
            passport.update(self.get_entries(line))
            if len(line) < 3 or line[-1] != '\n':
                self.pass_list.append(passport)
                passport = {}

    @staticmethod
    def get_entries(raw_data):
        entries_dict = {}
        for pair in raw_data.split():
            arr = pair.split(":")
            entries_dict[arr[0]] = arr[1]
        return entries_dict

    @staticmethod
    def is_valid(passport):
        for field in PassportManager.mandatory_fields:
            if field not in passport:
                return False
            if not PassportManager.checkers[field](passport[field]):
                return False

        for field in PassportManager.optional_fields:
            if field not in passport:
                continue
            if not PassportManager.checkers[field](passport[field]):
                return False

        return True

    def __len__(self):
        return len(self.pass_list)

    def __getitem__(self, index):
        return self.pass_list[index]

    def __iter__(self):
        return iter(self.pass_list)
