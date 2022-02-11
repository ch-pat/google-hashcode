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
        elif liked[ing] >= disliked[ing] * 1.0:
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


def greedy_solve(customers):
    # Takes almost 2 hours for file D but gets best result
    # Adds best ingredient in each loop
    result = []
    liked = {}
    disliked = {}
    all_ingredients = set([])
    
    # Build all ingredients set
    for customer in customers:
        for ing in customer.likes:
            add_ingredient(liked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
        for ing in customer.dislikes:
            add_ingredient(disliked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
    
    # add obvious ingredients to result
    to_remove = set([])
    for ing in all_ingredients:
        if ing not in disliked:
            result += [ing]
            to_remove = to_remove.union({ing})
        elif ing not in liked:
            continue
    all_ingredients = all_ingredients.difference(to_remove)
    
    best_ing = None
    best_score = calculate_score(result, customers)
    found_improvement = True

    while found_improvement:
        found_improvement = False
        best_ing = None
        for ing in all_ingredients:
            result.append(ing)
            cur_score = calculate_score(result, customers)
            if cur_score > best_score:
                best_score = cur_score
                result = result[:]
                best_ing = ing
                found_improvement = True
            result = result[:-1]
        if best_ing == None:
            break
        all_ingredients.remove(best_ing)
        result.append(best_ing)
        print(f"Best score improved to {best_score} by adding {best_ing}, {len(all_ingredients)} ingredients left to process.")

    return str(len(result)) + " " + " ".join(result)


def greedy_solve2(customers):
    # Takes less time than greedy solve 1 (4 minutes) and has better performance
    # Adds the first ingredient that increases score at each loop
    result = []
    liked = {}
    disliked = {}
    all_ingredients = set([])
    
    # Build all ingredients set
    for customer in customers:
        for ing in customer.likes:
            add_ingredient(liked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
        for ing in customer.dislikes:
            add_ingredient(disliked, ing, 1)
            all_ingredients = all_ingredients.union({ing})
    
    # add obvious ingredients to result
    to_remove = set([])
    for ing in all_ingredients:
        if ing not in disliked:
            result += [ing]
            to_remove = to_remove.union({ing})
        elif ing not in liked:
            to_remove = to_remove.union({ing})
            continue
    all_ingredients = all_ingredients.difference(to_remove)
    
    # Optimize below if anything
    best_score = calculate_score(result, customers)
    found_improvement = True
    found_ing = None
    guaranteed_score, customers = trim_customers(customers, set(result), all_ingredients)

    while found_improvement:
        found_ing = None
        found_improvement = False
        for ing in all_ingredients:
            result.append(ing)
            cur_score = guaranteed_score + calculate_score(result, customers)
            if cur_score > best_score:
                best_score = cur_score
                found_improvement = True
                found_ing = ing
                break
            else:
                result = result[:-1]
        if found_ing:
            all_ingredients.remove(found_ing)
            accrued_score, customers = trim_customers(customers, set(result), all_ingredients)
            guaranteed_score += accrued_score
        print(f"Best score improved to {best_score} by adding {found_ing}, {len(all_ingredients)} ingredients left to process.")

    # Maybe add a step for adding combinations of 2 ingredients
    # print("started work on combinations")
    # found_improvement = True
    # found_combo = None
    # while found_improvement:
    #     found_improvement = False
    #     found_combo = False
    #     for i in range(2, 4):
    #         for combo in itertools.combinations(all_ingredients, i):
    #             result += combo
    #             cur_score = calculate_score(result, customers)
    #             if cur_score >= best_score:
    #                 best_score = cur_score
    #                 found_improvement = True
    #                 found_combo = combo
    #                 break
    #             else:
    #                 result = result[:-i]
    #         if found_combo:
    #             all_ingredients = all_ingredients.difference(set(found_combo))
    #         print(f"Best score improved to {best_score} by adding {found_combo}, {len(all_ingredients)} ingredients left to process.")


    return str(len(result)) + " " + " ".join(result)


def brute_solve(customers):
    if len(customers) > 10:
        return "0 " + " ".join(customers[0].likes)
    
    all_ingredients = set([])
    # Build all ingredients set
    for customer in customers:
        for ing in customer.likes:
            all_ingredients = all_ingredients.union({ing})
        for ing in customer.dislikes:
            all_ingredients = all_ingredients.union({ing})
    
    best_score = 0
    result = []
    for i in range(len(all_ingredients) + 1):
        for comb in itertools.combinations(all_ingredients, i):
            cur_score = calculate_score(set(comb), customers)
            if cur_score > best_score:
                result = list(comb)
                best_score = cur_score
    print(f"Called brute solve for file with {len(customers)} customers; best result = {result}")
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

def calculate_score(solution, customers):
    if type(solution) == str:
        ingredients = set(solution.split()[1:])
    else:
        ingredients = set(solution)
    score = 0
    for c in customers:
        if c.likes_pizza(ingredients):
            score += 1
    return score


def trim_customers(customers, current_ingredients, all_ingredients) -> (int, list):
    # to make score calculation faster we want to remove customers that can't be included anymore
    # A customer is 100% included if the ingredients they dislike are not in ingredients and he likes current ingredients
    # A customer is 100% excluded if current_ingredients contains an ingredient they dislike
    # Must return the number of 100% included trimmed customers to keep track of score, and the trimmed list of customers
    guaranteed = 0
    to_remove = []
    for c in customers:
        if c.dislikes.isdisjoint(all_ingredients) and c.likes_pizza(current_ingredients):
            guaranteed += 1
            to_remove += [c]
        elif c.dislikes.intersection(current_ingredients):
            to_remove += [c]
    customers = list(set(customers).difference(set(to_remove)))
    print(f"Found {guaranteed} guaranteed customers, remaining: {len(customers)}")
    return guaranteed, customers

if __name__ == "__main__":
    pass
