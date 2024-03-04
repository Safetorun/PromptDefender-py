from typing import Optional
from pydantic import BaseModel

from xml_scanner import BasicXmlScanner
from prompt_validator import PromptValidator
from remote_wall_checker import PromptDefenderClient, WallResponse


class ValidationResult(BaseModel):
    contains_pii: Optional[bool] = None
    potential_jailbreak: bool
    potential_xml_escaping: Optional[bool] = None
    suspicious_user: Optional[bool] = None
    suspicious_session: Optional[bool] = None


class ValidatorExecutor(BaseModel):
    xml_scanner: BasicXmlScanner
    prompt_validator: PromptValidator
    remote_wall_checker: Optional[PromptDefenderClient] = None

    def execute_xml_scanner(self, prompt: str) -> bool:
        return self.xml_scanner.check_for_xml_tag(prompt)

    def execute_prompt_validator(self, prompt: str) -> bool:
        return self.prompt_validator.validate_prompt(prompt)

    def execute_remote_wall_checker(self, prompt: str) -> Optional[WallResponse]:
        if self.remote_wall_checker is not None:
            return self.remote_wall_checker.call_remote_wall(prompt)
        return None

    def execute_validators(self, prompt: str) -> ValidationResult:
        xml_injection_detected = self.execute_xml_scanner(prompt)
        prompt_validator_failed = not self.execute_prompt_validator(prompt)

        remote_wall_response = self.execute_remote_wall_checker(prompt)

        contains_pii: Optional[bool] = None
        potential_jailbreak: bool = False
        potential_xml_escaping: Optional[bool] = None
        suspicious_user: Optional[bool] = None
        suspicious_session: Optional[bool] = None

        if remote_wall_response is not None:
            contains_pii = remote_wall_response.contains_pii
            potential_jailbreak = remote_wall_response.potential_jailbreak
            potential_xml_escaping = remote_wall_response.potential_xml_escaping
            suspicious_user = remote_wall_response.suspicious_user
            suspicious_session = remote_wall_response.suspicious_session

        return ValidationResult(xml_injection_detected=xml_injection_detected,
                                prompt_validator_failed=prompt_validator_failed,
                                contains_pii=contains_pii,
                                potential_jailbreak=potential_jailbreak,
                                potential_xml_escaping=potential_xml_escaping,
                                suspicious_user=suspicious_user,
                                suspicious_session=suspicious_session
                                )
