from enum import Enum


class MatchLevel(Enum):
    """
    The match level for sagemaker debert responses
    """
    NoMatch = 0
    Medium = 1
    VeryClose = 2
    ExactMatch = 3


def match_level_for_score(score) -> MatchLevel:
    if score == 1.0:
        return MatchLevel.ExactMatch
    if score > 0.9:
        return MatchLevel.VeryClose
    if score > 0.5:
        return MatchLevel.Medium
    return MatchLevel.NoMatch
