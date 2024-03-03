from typing import Optional, List
from pydantic import BaseModel, validator


class PromptValidator(BaseModel):
    length: Optional[int] = None
    acceptable_values: Optional[List[str]] = None

    def validate_prompt(self, prompt: str) -> bool:
        if self.length is not None and len(prompt) > self.length:
            return False

        if self.acceptable_values is not None and prompt not in self.acceptable_values:
            return False

        return True
