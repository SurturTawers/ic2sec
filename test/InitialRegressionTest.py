"""
To run this test, go to src folder and execute python3 test/InitialRegressionTest.py

"""

import os
import sys
import unittest

sys.path.append(os.path.abspath('src'))

# To be tested.
from old.main import main as old_main
from Controller import Controller

class InitialRegressionTest(unittest.TestCase):

    def test_same_end_pops(self):
        """
        2022/05/18 - vcoopman
        Compares that result pop/models from both old and refactored code is the same.
        Its hard to check exactly as this methods include randomness.

        """

        old_models = old_main()

        # New models.
        populations = Controller().run()

        # first_ind_old = old_models[0].population[0]
        # print("First individual OLD: ")
        # print(first_ind_old)

        # first_ind = populations[0].individuals[0]
        # print("First individual: ")
        # print(first_ind)

        # self.assertEqual(first_ind_old, first_ind)

        normal_pop_old = old_models[0]
        print("NORMAL POPULATION OLD:")
        print(normal_pop_old)

        print("ATTACK POPULATION OLD:")
        attack_pop_old = old_models[1]
        print(attack_pop_old)

        print("NORMAL POPULATION:")
        normal_pop = populations[0]
        print(normal_pop)

        print("ATTACK POPULATION:")
        attack_pop = populations[1]
        print(attack_pop)

        self.assertEqual(attack_pop_old.repose, attack_pop.repose)
        print("Test passed, both implementations detected the attack.")

if __name__ == "__main__":
    unittest.main()

