from pydantic import BaseModel


class DrawbridgeResponse(BaseModel):
    is_safe: bool = False
    cleaned_response: str = ""


class DrawbridgeExecutor(BaseModel):
    """
    Drawbridge is a class that can be used to validate the response of an LLM execution
    """

    def validate_response_and_clean(self, response: str) -> DrawbridgeResponse:
        return DrawbridgeResponse(is_safe=True, cleaned_response=response)
