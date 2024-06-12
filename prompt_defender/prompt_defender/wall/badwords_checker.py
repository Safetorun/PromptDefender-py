import logging
from enum import Enum
from typing import Optional, Callable, List
from pydantic import BaseModel


class MatchLevel(Enum):
    ExactMatch = 0
    VeryClose = 1
    Medium = 2
    NoMatch = 3
    TotallyDifferent = 4


class ClosestMatchScore(BaseModel):
    match_description: str
    score: MatchLevel


class ClosestMatcher:
    def get_closest_match(self, text: str) -> Optional[ClosestMatchScore]:
        raise NotImplementedError("Subclasses should implement this method")


class BadWords(BaseModel):
    matcher: ClosestMatcher
    threshold: MatchLevel = MatchLevel.VeryClose
    logger: Optional[logging.Logger] = logging.getLogger(__name__)

    def check_prompt_contains_bad_words(self, prompt: str) -> Optional[bool]:
        self.logger.info(f"Going to check for bad words in prompt: {prompt}")
        try:
            score = self.matcher.get_closest_match(prompt)
            if score is None:
                return None
            contains_bad_word = score.score.value <= self.threshold.value
            return contains_bad_word
        except Exception as e:
            self.logger.error(f"Error while checking for bad words: {e}")
            return None


def create_bad_words(matcher: ClosestMatcher, **options) -> BadWords:
    return BadWords(matcher=matcher, **options)


# Example usage
class ExampleMatcher(ClosestMatcher):
    def get_closest_match(self, text: str) -> Optional[ClosestMatchScore]:
        # Dummy implementation
        if "badword" in text:
            return ClosestMatchScore(match_description="Found badword", score=MatchLevel.ExactMatch)
        return ClosestMatchScore(match_description="No badword found", score=MatchLevel.NoMatch)


matcher = ExampleMatcher()
bad_words_checker = create_bad_words(matcher=matcher)

prompt = "This is a badword in a prompt"
contains_bad_word = bad_words_checker.check_prompt_contains_bad_words(prompt)
print(f"Contains bad word: {contains_bad_word}")
