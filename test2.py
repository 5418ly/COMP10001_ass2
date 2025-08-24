from random import randint
from random import sample
import unittest
from Assigment2Q4 import Allocater

class TestAllocater(unittest.TestCase):

    def setUp(self):
        # Setting up sample populations for testing
        self.pops = []
        # self.subjs = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','A1','B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','M1','N1''A11','B11','C11','D11','E11','F11','G11','H11','I11','J11','K11','L11','M11','N11']
        self.subjs = ['A','B','C','D']
        for num in range(10):
            self.pops.append((randint(0,266),sample(self.subjs,randint(1,len(self.subjs)))))

    def test_large(self):

        allocater = Allocater(self.pops)
        print(allocater.alloc())

if __name__ == '__main__':
    unittest.main()
