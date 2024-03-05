import logging
from typing import Optional

from pydantic import BaseModel, Field


class BasicXmlScanner(BaseModel):
    xml_tag: Optional[str] = None
    logger: logging.Logger = Field(default_factory=lambda: logging.getLogger(__name__))

    class Config:
        arbitrary_types_allowed = True

    def check_for_xml_tag(self, prompt: str) -> bool:
        self.logger.info(f"Scanning text for tag: {self.xml_tag} in input: {prompt}")

        if not self.xml_tag:
            return False

        tag_to_scan_for = f"<{self.xml_tag}>"
        other_tag_to_scan_for = f"</{self.xml_tag}>"

        return tag_to_scan_for in prompt or other_tag_to_scan_for in prompt
