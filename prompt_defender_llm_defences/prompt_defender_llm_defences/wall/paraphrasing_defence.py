from typing import Optional

from prompt_defender import Defence
from langchain.llms import BaseLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ParaphrasingDefence(Defence):
    """
    Paraphrasing Defence which attempts to paraphrase a prompt to detect prompt injection.
    """

    llm: Optional[BaseLLM] = None

    def __init__(self, /, **data):
        super().__init__()
        self.llm = data["llm"]

    def check_user_input(self, instruction: str,
                         user_id: Optional[str] = None,
                         session_id: Optional[str] = None) -> (bool, str):
        """
        Defence for instruction prompt

        Returns:
            bool: if the instruction is safe to execute
        """
        prompt = PromptTemplate.from_template('Paraphrase the following text.\nText: {instruction}')
        chain = prompt | self.llm | StrOutputParser()

        return False, chain.invoke(input={"instruction": instruction})
