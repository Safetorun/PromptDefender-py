from typing import Optional, List, Callable

from ..core import WallExecutor, ValidationResult


class PromptValidator(WallExecutor):
    max_length: Optional[int] = None
    acceptable_values: Optional[List[str]] = None

    def validate_prompt(self, prompt: str,
                        xml_tag: Optional[str] = None,
                        user_id: Optional[str] = None,
                        session_id: Optional[str] = None) -> ValidationResult:
        """
        Validate a prompt

        :param prompt: The prompt to validate

        :return:
        """
        if self.max_length is not None and len(prompt) > self.max_length:
            return ValidationResult(unacceptable_prompt=True)

        if self.acceptable_values is not None and prompt not in self.acceptable_values:
            return ValidationResult(unacceptable_prompt=True)

        return ValidationResult(unacceptable_prompt=False)


def build_prompt_validator(max_length: Optional[int] = None,
                           acceptable_values: Optional[List[str]] = None) -> Callable[[], WallExecutor]:
    return lambda: PromptValidator(max_length=max_length, acceptable_values=acceptable_values)
