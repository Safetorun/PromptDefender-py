from typing import Optional

from prompt_defender import Defence
from langchain_core.language_models import BaseLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ParaphrasingDefence(Defence):
    """
    Paraphrasing Defence which attempts to paraphrase a prompt to detect prompt injection.
    """

    llm: Optional[BaseLLM] = None
    parser: Optional[StrOutputParser] = None

    def __init__(self, /, **data):
        super().__init__()
        self.llm = data["llm"]
        self.parser = data["parser"] or StrOutputParser()

    def is_user_input_safe(self, instruction: str,
                           user_id: Optional[str] = None,
                           session_id: Optional[str] = None) -> (bool, str):
        """
        Defence for instruction prompt

        Returns:
            bool: if the instruction is safe to execute - true if it is safe, false if it is not safe
        """
        prompt = PromptTemplate.from_template('Paraphrase the following text.\nText: {instruction}')
        chain = prompt | self.llm | self.parser

        return False, chain.invoke(input={"instruction": instruction})
