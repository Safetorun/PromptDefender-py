import logging
from typing import Optional

from pydantic import Field

from core import ValidationResult, WallExecutor


class BasicXmlScanner(WallExecutor):
    logger: logging.Logger = Field(default_factory=lambda: logging.getLogger(__name__))

    class Config:
        arbitrary_types_allowed = True

    def validate_prompt(self, prompt: str,
                        xml_tag: Optional[str] = None,
                        user_id: Optional[str] = None,
                        session_id: Optional[str] = None) -> ValidationResult:
        self.logger.info(f"Scanning text for tag: {xml_tag} in input: {prompt}")

        if not xml_tag:
            return ValidationResult(unacceptable_prompt=False)

        tag_to_scan_for = f"<{xml_tag}>"
        other_tag_to_scan_for = f"</{xml_tag}>"

        return ValidationResult(unacceptable_prompt=tag_to_scan_for in prompt or other_tag_to_scan_for in prompt)


def build_xml_scanner() -> BasicXmlScanner:
    return BasicXmlScanner()
