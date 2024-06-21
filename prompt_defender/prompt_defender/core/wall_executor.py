from typing import Optional, Callable, List

from pydantic import BaseModel


class ValidationResult(BaseModel):
    unacceptable_prompt: bool = False
    modified_prompt: str


class WallExecutor(BaseModel):
    def is_user_input_safe(self, prompt: str,
                        xml_tag: Optional[str] = None,
                        user_id: Optional[str] = None,
                        session_id: Optional[str] = None) -> ValidationResult:
        return ValidationResult(potential_jailbreak=False, modified_prompt=prompt)


class CompositeWallExecutorBuilder(BaseModel):
    wall_executors: List[Callable[[], WallExecutor]] = []

    def add_wall_executor(self, wall_executor: Callable[[], WallExecutor]):
        self.wall_executors.append(wall_executor)

    def build(self) -> List[Callable[[], WallExecutor]]:
        return self.wall_executors
