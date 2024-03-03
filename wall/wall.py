from pydantic import BaseModel

from xml_scanner import BasicXmlScanner
from prompt_validator import PromptValidator


class ValidationResult(BaseModel):
    xml_injection_detected: bool
    prompt_validator_failed: bool


class ValidatorExecutor(BaseModel):
    xml_scanner: BasicXmlScanner
    prompt_validator: PromptValidator

    def execute_xml_scanner(self, prompt: str) -> bool:
        return self.xml_scanner.check_for_xml_tag(prompt)

    def execute_prompt_validator(self, prompt: str) -> bool:
        return self.prompt_validator.validate_prompt(prompt)

    def execute_validators(self, prompt: str) -> ValidationResult:
        xml_injection_detected = self.execute_xml_scanner(prompt)
        prompt_validator_failed = not self.execute_prompt_validator(prompt)

        return ValidationResult(xml_injection_detected=xml_injection_detected,
                                prompt_validator_failed=prompt_validator_failed)
