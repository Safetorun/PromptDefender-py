from typing import Optional, List
from pydantic import BaseModel, validator
import logging


class BasicXmlScanner(BaseModel):
    xml_tag: Optional[str] = None
    logger = logging.getLogger(__name__)

    def check_for_xml_tag(self, prompt: str) -> bool:
        self.logger.info(f"Scanning text for tag: {self.xml_tag} in input: {prompt}")

        result = False
        if self.xml_tag:
            tag_to_scan_for = f"<{self.xml_tag}>"
            other_tag_to_scan_for = f"</{self.xml_tag}>"
            result = tag_to_scan_for in prompt or other_tag_to_scan_for in prompt

        return result
