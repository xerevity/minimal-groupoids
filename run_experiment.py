from io import TextIOWrapper
from tqdm import tqdm
import random

random.seed(0)

class Grupoid:
    def __init__(self, matrix):
        self.order = len(matrix)
        for row in matrix:
            if len(row) != self.order:
                raise Exception(
                    "Wrong initialization: row lengths do not match the order."
                    )
        

        switcher = {
                        "a": 0,
                        "b": 1,
                        "c": 2,
                        "d": 3,
                        "e": 4,
                        "f": 5,
                        "g": 6,
                        "h": 7,
                        "0": 0,
                        "1": 1,
                        "2": 2,
                        "3": 3,
                        "4": 4,
                        "5": 5,
                        "6": 6,
                    }

        s = []
        for row in matrix:
            if type(row[0]) == str:
                s.append(tuple([switcher[e] for e in row]))
            else: s.append(tuple(row))

        self.matrix = tuple(s)

        elems = set()
        for row in self.matrix:
            for elem in row:
                elems.add(elem)
                
        self.elements = sorted(list(elems))


    def __eq__(self, other):
        if not isinstance(other, Grupoid):
            # don't attempt to compare against unrelated types
            raise NotImplementedError

        return self.matrix == other.matrix


    def __str__(self):
        s = 2 * self.order * "_" + "\n"

        for row in self.matrix:
            s += "|"
            s += " ".join([str(e) for e in row])
            s += "\n"
        return s

  
    def product(self, x, y):
        
        if type(x) == type(y) == int:
            return self.matrix[self.elements.index(x)][self.elements.index(y)]
    
        else:
            print(type(x), type(y))
            raise Exception("Wrong product arguments.")


def __hash__(self):
        return hash(self.matrix)

def product_grupoid(left: Grupoid, right: Grupoid, multiplicator: Grupoid):
    
    assert left.order == right.order == multiplicator.order

    matrix = []
    for row_left, row_right in zip(left.matrix, right.matrix):
        row = []
        for x, y in zip(row_left, row_right):
            row.append(multiplicator.product(x, y))
        matrix.append(row)

    return(Grupoid(matrix))

def generated_grupoids(start_set: set, multiplicator: Grupoid):
    depth = 0

    while(True):
        new_set = set()
        depth += 1
        for grup1 in start_set:
            for grup2 in start_set:
                new_set.add(product_grupoid(Grupoid(grup1), Grupoid(grup2), multiplicator).matrix)

        if new_set.issubset(start_set):
            break

        start_set = new_set.union(start_set)
        #print(len(start_set))
    #print(depth)
    return(start_set)



def r_zero(elems):
    if type(elems) == int:
        n = elems
        matrix = [list(range(n)) for _ in range(n)]
        return Grupoid(matrix)
    else:
        matrix = [sorted(list(elems)) for _ in range(len(elems))]
        return Grupoid(matrix)


def l_zero(elems):
    if type(elems) == int:
        n = elems
        matrix = [list([i for _ in range(n)]) for i in range(n)]
        return Grupoid(matrix)
    else:
        matrix = [list([i for _ in range(len(elems))]) for i in sorted(list(elems))]
        return Grupoid(matrix)
    

def random_idempotent_grupoid(n: int):
    matrix = [[random.randint(0,n-1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = i
    return Grupoid(matrix)


def is_minimal_clone(matrix_set: set):
    g = list(matrix_set)[0]
    n = len(g[0])
    start_set = {r_zero(n).matrix, l_zero(n).matrix}

    for g in matrix_set.difference(start_set):
        if generated_grupoids(start_set, Grupoid(g)) != matrix_set:
            return False
    return True


def random_product(k: int, mul_grupoid: Grupoid):
    n = mul_grupoid.order

    if k==1:
        return random.choice([l_zero, r_zero])(n)

    elif k > 1:
        return product_grupoid(random_product(k-1, mul_grupoid), random_product(k-1, mul_grupoid), mul_grupoid)


def product_walk(k: int, mul_grupoid: Grupoid):
    n = mul_grupoid.order
    g = mul_grupoid

    for _ in range(10):
        g = random_product(10, g)
        
    for i in range(k-10):
        g = random_product(10, g)
        if is_minimal_clone(generated_grupoids({r_zero(n).matrix, l_zero(n).matrix}, g)):
                break
    return g


n = 6

minimal = 0
nonminimal = 0

minimalf = TextIOWrapper = open("minimal6.txt", "w")
nonminimalf = TextIOWrapper = open("nonminimal6.txt", "w")

for i in tqdm(range(1001)):
    g = random_idempotent_grupoid(n)
    if i == 808:
        print(g)
        continue


    lim = product_walk(1000, g)

    # check minimality
    if is_minimal_clone(generated_grupoids({l_zero(n).matrix, r_zero(n).matrix}, lim)):
        minimal += 1
        print(lim, file=minimalf)
    else: 
        nonminimal += 1
        print(lim, file=nonminimalf)

print(minimal, nonminimal)

minimalf.close()
nonminimalf.close()
