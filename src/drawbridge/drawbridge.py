import bleach
from pydantic import BaseModel


def __check_for_canary__(canary: str, llm_response: str) -> bool:
    return canary in llm_response


class Drawbridge(BaseModel):
    """
    Drawbridge is a class that can be used to validate the response of an LLM execution
    """
    canary: str
    allow_unsafe_scripts: bool = False

    def validate_response_and_clean(self, response: str) -> (bool, str):
        response_ok = __check_for_canary__(self.canary, response)

        if not self.allow_unsafe_scripts:
            response = bleach.clean(response, strip=True)

        return response_ok, response
