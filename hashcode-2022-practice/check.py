from solver import hyper_solve as solve
from solver import brute_solve
from solver import calculate_score
from parse import parse_file
import os
import time
import json

IN_DIR = "input/"
OUT_DIR = "output/"
TOP_SCORES = "best_scores.json"
TOP_SOLVES = "best_solutions.json"

if __name__ == "__main__":
    files = os.listdir(IN_DIR)
    #files.remove("e_elaborate.in.txt")
    easy_files = sorted(files)[0:3]
    hard_files = sorted(files)[3:]

    # Save / Load best scores and solutions files
    if TOP_SCORES not in os.listdir():
        with open(TOP_SCORES, "w+") as f:
            json.dump({f: 0 for f in files}, f)
    with open(TOP_SCORES, "r") as f:
        best_scores = json.load(f)

    if TOP_SOLVES not in os.listdir():
        with open(TOP_SOLVES, "w+") as f:
            json.dump({f: "" for f in files}, f)
    with open(TOP_SOLVES, "r") as f:
        best_solves = json.load(f)
    
    # Solve for all files
    for f in files:
        start = time.time()
        customers = parse_file(IN_DIR + f)
        
        if f in easy_files:
            solution = brute_solve(customers)
        else:
            solution = solve(customers)
        print(f"Completed file {f} in {time.time() - start} seconds")

        score = calculate_score(solution, customers)
        print(f"Score for file {f} = {score} -- (current best: {best_scores[f]})")
        if score > best_scores[f]:
            print(f"### NEW BEST SCORE FOR FILE {f}: {score} -- (previous best: {best_scores[f]}) ###")
            best_scores[f] = score
            best_solves[f] = solution
            with open(TOP_SCORES, "w") as outfile:
                json.dump(best_scores, outfile)
            with open(TOP_SOLVES, "w") as outfile:
                json.dump(best_solves, outfile)
            

        print()
        with open(OUT_DIR + f, "w+") as f:
            f.writelines(solution)
