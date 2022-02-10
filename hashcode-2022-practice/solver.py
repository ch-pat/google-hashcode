from parse import parse_file
import os
import itertools

def solve(i):
    ingredients = {}
    for customer in i:
        for ing in customer.likes:
            add_ingredient(ingredients, ing, 1)
        for ing in customer.dislikes:
            add_ingredient(ingredients, ing, -1)
    return parse_ingredients(ingredients)


def solve2(i):
    liked = {}
    disliked = {}
    all_ingredients = set([])
    result = []
    for customer in i:
        for ing in customer.likes:
            add_ingredient(liked, ing, 1 / len(customer.likes))
            all_ingredients = all_ingredients.union({ing})
        for ing in customer.dislikes:
            add_ingredient(disliked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
    for ing in all_ingredients:
        if ing not in disliked:
            result += [ing]
        elif ing not in liked:
            continue
        elif liked[ing] >= disliked[ing] * 0.5:
            result += [ing]
    return str(len(result)) + " " + " ".join(result)

def solve3(i):
    liked = {}
    disliked = {}
    all_ingredients = set([])
    result = []
    for customer in i:
        for ing in customer.likes:
            add_ingredient(liked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
        for ing in customer.dislikes:
            add_ingredient(disliked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
    for ing in all_ingredients:
        if ing not in disliked:
            result += [ing]
        elif ing not in liked:
            continue

    candidates = all_ingredients.difference(set(result))
    candidates_list = list(candidates)

    mixed_likes = {}
    for comb in itertools.combinations(candidates_list, 2):
        a, b = comb
        mixed_likes[comb] = [0, 0]
        for c in i:
            if a in c.likes and b in c.dislikes:
                mixed_likes[comb][0] += 1
            if b in c.likes and a in c.dislikes:
                mixed_likes[comb][1] += 1
    for comb in mixed_likes:
        if abs(mixed_likes[comb][0] - mixed_likes[comb][1]) <= int(len(i) / 20):
            result += [comb[0]]
        else:
            if mixed_likes[comb][0] > mixed_likes[comb][1]:
                result += [comb[0]]
            else:
                result += [comb[1]]
    result = list(set(result))
    return str(len(result)) + " " + " ".join(result)


def add_ingredient(ingredients_dict, ingredient, score):
    if ingredient not in ingredients_dict:
        ingredients_dict[ingredient] = score
    else:
        ingredients_dict[ingredient] += score
    return ingredients_dict

def parse_ingredients(ingredients_dict):
    out = [ing for ing, score in ingredients_dict.items() if score > 0]
    return str(len(out)) + " " + " ".join(out)



if __name__ == "__main__":
    pass
