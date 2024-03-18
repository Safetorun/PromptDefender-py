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


def build_drawbridge(canary: str, allow_unsafe_scripts: bool = False) -> Drawbridge:
    """
    Factory function to build a Drawbridge object

    :param canary: what to look for in the response to validate if a canary was returned
    :param allow_unsafe_scripts: whether or not to allow scripts in the response. If False, scripts will be removed

    :return: Drawbridge object which you can call validate_response_and_clean oon to validate and clean the response
    """
    return Drawbridge(canary=canary, allow_unsafe_scripts=allow_unsafe_scripts)
