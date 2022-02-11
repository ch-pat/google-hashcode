class Customer:
    def __init__(self, likes, dislikes):
        self.likes: set = likes
        self.dislikes: set = dislikes

    def likes_pizza(self, ingredients: set):
        # Order here is important! isdisjoint will usually be faster than issubset.
        return self.dislikes.isdisjoint(ingredients) and self.likes.issubset(ingredients)


    def __str__(self):
        return str(self.likes) + " " + str(self.dislikes)


def parse_file(filepath: str):
    with open(filepath, "r") as f:
        lines = f.read().split("\n")
    n_clients = lines[0]
    if lines[-1] == "":
        lines = lines[:-1]
    clients = []
    for i in range(1, len(lines), 2):
        likes = lines[i].split()
        dislikes = lines[i + 1].split()
        likes = set(likes[1:])
        dislikes = set(dislikes[1:])
        c = Customer(likes, dislikes)
        clients += [c]
    return clients



if __name__ == "__main__":    
    clients = parse_file("input/a_an_example.in.txt")
    for c in clients:
        print(c)