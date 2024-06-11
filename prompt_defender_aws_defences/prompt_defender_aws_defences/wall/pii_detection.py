from typing import List
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from prompt_defender.core import WallExecutor, ValidationResult
from pydantic import BaseModel
from pydantic import Field


class PiiEntity(BaseModel):
    """
    PII entity
    """
    Type: str
    Score: float


class ScanResult(BaseModel):
    """
    Scan result
    """
    containing_pii: bool
    entities: Optional[List[PiiEntity]] = Field(default_factory=list)


class AwsPIIScanner(BaseModel):
    """
    A class that scans text for PII using AWS Comprehend.
    """

    def scan(self, text_to_scan: str) -> ScanResult:
        try:
            session = boto3.Session(region_name="eu-west-1")
            comprehend = session.client('comprehend')
            input_params = {
                'Text': text_to_scan,
                'LanguageCode': 'en'
            }
            output = comprehend.detect_pii_entities(**input_params)

            entities = [PiiEntity(Type=entity['Type'], Score=entity['Score']) for entity in output['Entities']]
            containing_pii = len(entities) > 0

            return ScanResult(containing_pii=containing_pii, entities=entities)

        except (BotoCoreError, ClientError) as e:
            print("Error detecting PII:", e)
            return ScanResult(containing_pii=False, entities=[])


class AwsPIIScannerWallExecutor(WallExecutor):
    """
    WallExecutor that scans text for PII using AWS Comprehend.
    """
    pii_scanner: Optional[AwsPIIScanner] = None

    def __init__(self):
        """
        The constructor for the AwsPIIScannerWallExecutor class.
        """
        super().__init__()
        self.pii_scanner = AwsPIIScanner()

    def is_user_input_safe(self, prompt: str,
                        xml_tag: Optional[str] = None,
                        user_id: Optional[str] = None,
                        session_id: Optional[str] = None) -> ValidationResult:
        result = self.pii_scanner.scan(prompt)
        return ValidationResult(unacceptable_prompt=result.containing_pii, modified_prompt=prompt)
