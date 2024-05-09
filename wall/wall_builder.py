from typing import Optional, List

from .wall_executor import WallExecutor
from .prompt_validator import PromptValidator
from .xml_scanner import BasicXmlScanner
from .prompt_defender_client import PromptDefenderClient
from .prompt_defender_client_rapidapi import PromptDefenderClientRapidApi, rapid_api_check


def create_wall(
        remote_jailbreak_check: bool = False,
        allow_pii: Optional[bool] = None,
        xml_tag: Optional[str] = None,
        api_key: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        max_prompt_length: Optional[int] = None,
        allowed_prompt_values: Optional[List[str]] = None,
        check_badwords: Optional[bool] = None,
        fast_check: Optional[bool] = None
) -> WallExecutor:
    """
    Create a wall with the given configuration

    :param allow_pii: Whether to allow PII to be scanned
    :param xml_tag: The XML tag to scan for
    :param api_key: The API key to use for the remote wall checker
    :param user_id: The user ID to use for the remote wall checker
    :param session_id: The session ID to use for the remote wall checker
    :param max_prompt_length: The maximum length of a prompt
    :param allowed_prompt_values: A list of allowed prompt values

    :return: A new wall with the given configuration
    """
    scanner: Optional[BasicXmlScanner] = None
    remote_wall_checker: Optional[PromptDefenderClient] = None
    prompt_validator: Optional[PromptValidator] = None

    if xml_tag is not None:
        scanner = BasicXmlScanner(xml_tag=xml_tag)

    if remote_jailbreak_check:
        remote_wall_checker = PromptDefenderClient(
            scan_pii=allow_pii,
            api_key=api_key,
            user_id=user_id,
            session_id=session_id,
            check_badwords=check_badwords,
            fast_check=fast_check
        )

    if max_prompt_length is not None or allowed_prompt_values is not None:
        prompt_validator = PromptValidator(
            max_prompt_length=max_prompt_length,
            allowed_prompt_values=allowed_prompt_values)

    if scanner is None and remote_wall_checker is None and prompt_validator is None:
        raise ValueError(
            "At least one of xml_tag, api_key, user_id, session_id, allow_pii, max_prompt_length, or allowed_prompt_values must be provided")

    return WallExecutor(
        xml_scanner=scanner,
        prompt_validator=prompt_validator,
        remote_wall_checker=remote_wall_checker,
    )
