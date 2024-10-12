import unittest
from ..wall.shared import MatchLevel, match_level_for_score


class TestMatchLevel(unittest.TestCase):

    def test_match_level_exact_match(self):
        self.assertEqual(match_level_for_score(1.0), MatchLevel.ExactMatch)

    def test_match_level_very_close(self):
        self.assertEqual(match_level_for_score(0.95), MatchLevel.VeryClose)
        self.assertEqual(match_level_for_score(0.9), MatchLevel.Medium)

    def test_match_level_medium(self):
        self.assertEqual(match_level_for_score(0.75), MatchLevel.Medium)
        self.assertEqual(match_level_for_score(0.6), MatchLevel.Medium)

    def test_match_level_no_match(self):
        self.assertEqual(match_level_for_score(0.5), MatchLevel.NoMatch)
        self.assertEqual(match_level_for_score(0.49), MatchLevel.NoMatch)
        self.assertEqual(match_level_for_score(0.0), MatchLevel.NoMatch)


if __name__ == '__main__':
    unittest.main()