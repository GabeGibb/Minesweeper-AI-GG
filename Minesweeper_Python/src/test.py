import itertools

list = [1, 2, 3]
# for i in range(len(list) + 1):
for subset in itertools.combinations(list, 2):
    # if (len(subset) == 2):
    print(subset)