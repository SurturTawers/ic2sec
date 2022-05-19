import unittest
import os
import sys

sys.path.append(os.path.abspath('src'))

# To be tested.
from old.main import main as old_main

class InitialRegressionTest(unittest.TestCase):

    def test_same_end_pops(self):
        """
        Compares that result pop/models from both old and refactored code is the same.

        2022/05/18
        """

        old_models = old_main()
        print(old_models)

        # New models.
        # models = main()


if __name__ == "__main__":
    unittest.main()

