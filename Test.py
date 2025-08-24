import unittest
import numpy as np
# from Assigment2Q1 import zbini_attrs  # Assuming this module provides the zbini attributes
from Assigment2B2_copy import Allocater, alloc_study_groups  # Replace 'your_module' with the actual module name
from random import randint
from random import sample

class TestAllocater(unittest.TestCase):

    def setUp(self):
        # Setting up sample populations for testing
        self.population1 = [
            (34, ['math', 'science']),
            (34, ['math', 'english']),
            (34, ['science', 'art']),
            (34, ['art', 'english']),
            (34, ['math', 'art']),
            (34, ['science', 'english']),
        ]
        self.empty_population = []
        self.single_population = [(0, ['math', 'science'])]
        self.no_common_subjects = [
            (0, ['math']),
            (1, ['science']),
            (2, ['english']),
            (3, ['art']),
        ]

    def test_initialization(self):
        allocater = Allocater(self.population1)
        self.assertEqual(allocater._pop, self.population1)
        self.assertEqual(allocater._pop_size, len(self.population1))

    def test_validate_group(self):
        allocater = Allocater(self.population1)
        self.assertEqual(allocater.validate_group((0, 1, 2)), (False, None))
        self.assertEqual(allocater.validate_group((0, 1, 3)), (False, None))
        self.assertEqual(allocater.validate_group((0, 1, 4, 5)), (False, None))

    def test_form_study_group(self):
        allocater = Allocater(self.population1)
        study_groups = allocater.form_study_group()
        expected_groups = [((0, 1, 4), 4), ((0, 2, 5), 4), ((1, 3, 5), 4), ((2, 3, 4), 4)]
        self.assertEqual(study_groups, expected_groups)

    def test_alloc_group(self):
        allocater = Allocater(self.population1)
        allocated_group = allocater.alloc_group()
        expected_allocation = [
            (0, 1, 4),  # Example expected output, adjust as per actual logic
        ]
        self.assertEqual(allocated_group, expected_allocation)

    def test_empty_population(self):
        allocater = Allocater(self.empty_population)
        self.assertEqual(allocater.alloc_group(), [])

    def test_single_population(self):
        allocater = Allocater(self.single_population)
        self.assertEqual(allocater.alloc_group(), [])

    def test_no_common_subjects(self):
        allocater = Allocater(self.no_common_subjects)
        self.assertEqual(allocater.alloc_group(), [])

    def test_alloc_study_groups(self):
        result = alloc_study_groups(self.population1)
        expected_result = [
            (0, 1, 4),  # Example expected output, adjust as per actual logic
        ]
        self.assertEqual(result, expected_result)

    def test_large(self):
        pops = []
        subjs = ['A','B','C','D','E','F','G']
        for num in range(1000):
            pops.append((randint(0,255),sample(subjs,randint(1,7))))
        allocater = Allocater(pops)
        allocater.alloc_group()

if __name__ == '__main__':
    unittest.main()