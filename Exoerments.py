import numpy as np
from itertools import combinations

def has_common_subjects(v1, v2):
    # Check if two people have at least one subject in common
    return np.any(np.bitwise_and(v1, v2))

def valid_group(group, matrix):
    # Check every combination in the group for common subjects
    for p1, p2 in combinations(group, 2):
        if not has_common_subjects(matrix[:, p1], matrix[:, p2]):
            return False
    return True

def find_groups(matrix):
    n = matrix.shape[1]  # number of people
    valid_groups = []
    # Check all combinations for triples and quadruples
    for size in [3, 4]:
        for group in combinations(range(n), size):
            if valid_group(group, matrix):
                valid_groups.append(group)
    return valid_groups

# Example Matrix (each column is a person, each row a subject)
matrix = np.array([
    [1, 0, 1, 0, 1],
    [0, 1, 1, 1, 0],
    [1, 1, 0, 1, 0],
])

# Find and print valid groups
groups = find_groups(matrix)
print("Valid study groups are:", groups)