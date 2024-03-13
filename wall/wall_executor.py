from typing import Optional

from pydantic import BaseModel

from .prompt_defender_client import PromptDefenderClient, WallResponse
from .prompt_validator import PromptValidator
from .xml_scanner import BasicXmlScanner


class ValidationResult(BaseModel):
    contains_pii: Optional[bool] = None
    potential_jailbreak: bool
    potential_xml_escaping: Optional[bool] = None
    suspicious_user: Optional[bool] = None
    suspicious_session: Optional[bool] = None


def should_block_prompt(validation_result: ValidationResult) -> bool:
    return validation_result.contains_pii or \
        validation_result.potential_jailbreak or \
        validation_result.potential_xml_escaping or \
        validation_result.suspicious_user or \
        validation_result.suspicious_session


class WallExecutor(BaseModel):
    xml_scanner: Optional[BasicXmlScanner] = None
    prompt_validator: Optional[PromptValidator] = None
    remote_wall_checker: Optional[PromptDefenderClient] = None

    def __execute_xml_scanner__(self, prompt: str) -> bool:
        if self.xml_scanner is not None:
            return self.xml_scanner.check_for_xml_tag(prompt)
        else:
            return False

    def __execute_prompt_validator__(self, prompt: str) -> bool:
        if self.prompt_validator is not None:
            return self.prompt_validator.validate_prompt(prompt)
        else:
            return False

    def __execute_remote_wall_checker__(self, prompt: str) -> Optional[WallResponse]:
        if self.remote_wall_checker is not None:
            return self.remote_wall_checker.call_remote_wall(prompt)
        return None

    def validate_prompt(self, prompt: str) -> ValidationResult:
        """
        Validate a prompt
        :param prompt: The prompt to validate
        :return: validation result
        """
        xml_injection_detected = self.__execute_xml_scanner__(prompt)
        prompt_validator_failed = not self.__execute_prompt_validator__(prompt)
        remote_wall_response = self.__execute_remote_wall_checker__(prompt)

        contains_pii: Optional[bool] = None
        potential_jailbreak: bool = False
        suspicious_user: Optional[bool] = None
        suspicious_session: Optional[bool] = None

        if remote_wall_response is not None:
            contains_pii = remote_wall_response.contains_pii
            potential_jailbreak = remote_wall_response.potential_jailbreak
            suspicious_user = remote_wall_response.suspicious_user
            suspicious_session = remote_wall_response.suspicious_session

        return ValidationResult(potential_xml_escaping=xml_injection_detected,
                                prompt_validator_failed=prompt_validator_failed,
                                contains_pii=contains_pii,
                                potential_jailbreak=potential_jailbreak,
                                suspicious_user=suspicious_user,
                                suspicious_session=suspicious_session)
