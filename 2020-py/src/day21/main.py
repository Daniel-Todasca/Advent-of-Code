from src.helper import IO
import re


def parse_line(str_line):
    match = re.match(r"(.+)\(contains (.+)\)", str_line)
    return match.group(1).split(), match.group(2).replace(",", " ").split()


foods = []
translations = dict()
allergen_set = set()

for line in IO.read_all():
    ingredients, allergens = parse_line(line)
    foods.append((set(ingredients), allergens))
    allergen_set.update(allergens)

while len(allergen_set) > 0:
    to_remove = []
    for allergen in allergen_set:
        containing_foods = [food for food in foods if allergen in food[1]]
        union = set.intersection(*[food[0] for food in containing_foods])

        if len(union) == 1:
            translation = list(union)[0]
            translations[allergen] = translation
            to_remove.append(allergen)

            for food in foods:
                if translation in food[0]:
                    food[0].remove(translation)

    for task in to_remove:
        allergen_set.remove(task)

IO.write(len([ingredient for food in foods for ingredient in food[0] if ingredient not in translations.values()]))
IO.write(",".join(pair[1] for pair in sorted(translations.items(), key=lambda x: x[0])))
