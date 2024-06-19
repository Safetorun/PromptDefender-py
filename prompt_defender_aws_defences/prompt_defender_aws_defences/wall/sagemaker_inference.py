import json
from typing import Optional

import boto3
from prompt_defender.core import WallExecutor, ValidationResult
from pydantic import BaseModel

from .shared import match_level_for_score, MatchLevel


class RemoteSagemakerCaller(BaseModel):
    endpoint_url: str

    def query(self, payload: str):
        session = boto3.Session(region_name='eu-west-1')
        sm = session.client('sagemaker-runtime')
        input_bytes = json.dumps(payload).encode('utf-8')
        response = sm.invoke_endpoint(
            EndpointName=self.endpoint_url,
            ContentType='application/json',
            Body=input_bytes
        )
        response_body = json.loads(response['Body'].read().decode())

        for re in response_body:
            if re['label'] == 'INJECTION':
                return re['score']
            elif re['label'] == 'LEGIT':
                score = 1.0 - re['score']
                return score

        error_message = f"Could not find the label in the response. Response: {response_body}"
        raise ValueError(error_message)

    def call_remote_api(self, prompt) -> MatchLevel:
        response = self.query({'inputs': prompt})
        return match_level_for_score(response)


class SagemakerWallExecutor(WallExecutor):
    """
    WallExecutor that calls a remote SageMaker endpoint to validate the prompt.
    """
    sagemaker: Optional[RemoteSagemakerCaller] = None

    def __init__(self, sagemaker_name: str):
        """
        The constructor for the SagemakerWallExecutor class.

        :param sagemaker_name: The name of the SageMaker endpoint to call.
        """
        super().__init__()
        self.sagemaker = RemoteSagemakerCaller(endpoint_url=sagemaker_name)

    def is_user_input_safe(self, prompt: str,
                        xml_tag: Optional[str] = None,
                        user_id: Optional[str] = None,
                        session_id: Optional[str] = None) -> ValidationResult:
        result = self.sagemaker.call_remote_api(prompt)
        unacceptable_prompt = (result == MatchLevel.ExactMatch or result == MatchLevel.VeryClose)

        return ValidationResult(unacceptable_prompt=unacceptable_prompt, modified_prompt=prompt)
