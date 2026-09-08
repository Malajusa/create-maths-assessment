import unittest
from pathlib import Path

from scripts.run_regression_fixtures import run_fixtures

ROOT = Path(__file__).resolve().parents[1]


class RegressionFixtureTests(unittest.TestCase):
    def test_all_known_fixtures_match_expected_outcome(self):
        results = run_fixtures(ROOT)
        self.assertEqual(4, len(results))
        self.assertTrue(all(result["passed"] for result in results), results)


if __name__ == "__main__":
    unittest.main()
