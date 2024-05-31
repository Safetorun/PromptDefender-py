from typing import Optional, Callable, List

from pydantic import BaseModel

from .drawbridge_executor import DrawbridgeExecutor, DrawbridgeResponse
from .keep_executor import KeepExecutor, SafePromptResponse
from .wall_executor import WallExecutor


class Defence(BaseModel):
    keep: Optional[Callable[[], KeepExecutor]] = None
    wall: Optional[List[Callable[[], WallExecutor]]] = None
    drawbridge: Optional[Callable[[str], DrawbridgeExecutor]] = None

    base_prompt: Optional[SafePromptResponse] = None

    def prepare_prompt(self, prompt) -> SafePromptResponse:
        """
        :param prompt:
        :return:
        """
        if self.keep:
            response = self.keep().generate_prompt(prompt)
        else:
            response = SafePromptResponse(safe_prompt=prompt)

        self.base_prompt = response

        return response

    def check_user_input(self, instruction: str,
                         user_id: Optional[str] = None,
                         session_id: Optional[str] = None) -> bool:
        """
        Defence for instruction prompt

        Returns:
            bool: if the instruction is safe to execute
        """
        if self.wall:
            for wall in self.wall:
                if wall().validate_prompt(instruction, self.base_prompt.xml_tag, user_id,
                                          session_id).unacceptable_prompt:
                    return False
        return True

    def check_prompt_output(self, instruction: str) -> DrawbridgeResponse:
        """
        Defence for instruction prompt

        Returns:
            bool: if the instruction is safe to execute
            str: a cleaned version of the instruction
        """
        if self.drawbridge:
            return self.drawbridge(self.base_prompt.canary).validate_response_and_clean(instruction)

        return DrawbridgeResponse(is_safe=True, cleaned_response=instruction)
