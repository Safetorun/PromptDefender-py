from typing import Callable, Optional

import bleach

from ..core import DrawbridgeExecutor, DrawbridgeResponse


def __check_for_canary__(canary: str, llm_response: str) -> bool:
    return canary in llm_response


class DefaultDrawbridgeExecutor(DrawbridgeExecutor):
    """
    Drawbridge is a class that can be used to validate the response of an LLM execution
    """
    canary: Optional[str] = None
    allow_unsafe_scripts: bool = False

    def validate_response_and_clean(self, response: str) -> DrawbridgeResponse:
        if self.canary:
            response_ok = __check_for_canary__(self.canary, response)
        else:
            response_ok = True

        if not self.allow_unsafe_scripts:
            response = bleach.clean(response, strip=True)

        return DrawbridgeResponse(is_safe=response_ok, cleaned_response=response)


def _build_drawbridge(canary: Optional[str], allow_unsafe_scripts: bool = False) -> DrawbridgeExecutor:
    """
    Factory function to build a Drawbridge object

    :param canary: what to look for in the response to validate if a canary was returned
    :param allow_unsafe_scripts: whether or not to allow scripts in the response. If False, scripts will be removed

    :return: Drawbridge object which you can call validate_response_and_clean oon to validate and clean the response
    """
    return DefaultDrawbridgeExecutor(canary=canary, allow_unsafe_scripts=allow_unsafe_scripts)


def build_drawbridge(allow_unsafe_scripts: bool = False) -> Callable[[str], DrawbridgeExecutor]:
    """
    Factory function to build a Drawbridge object

    :param allow_unsafe_scripts: whether or not to allow scripts in the response. If False, scripts will be removed

    :return: Drawbridge object which you can call validate_response_and_clean oon to validate and clean the response
    """
    return lambda x: _build_drawbridge(x, allow_unsafe_scripts=allow_unsafe_scripts)
