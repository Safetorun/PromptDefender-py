import os.path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders.directory import DirectoryLoader

prompt = PromptTemplate.from_template(
    """I am going to give you a prompt which is used in an LLM application. I want you to take this prompt,
    and generate a single question that a user might realistically send to the application.
    
    Use placeholders if they are there to assume that those placeholders are filled in with the user input. If there
    are no placeholders, assume that the prompt will be compiled with the <prompt> provided, with the user input just
    appended to the end.
    
    Previously sent prompts:
    {previous_prompts}
    
    Here is the prompt:
    <prompt>
        {prompt}
    </prompt>
    
    * Return only the generated user input
    * These test cases will be taken sent exactly as they are - so not extraneous information is required
    * Return exactly one example
    """
)

numb = 5

if not os.path.exists("prompts"):
    os.makedirs("prompts")


def docs_to_prompts(docs):
    return "\n\n".join([doc.page_content for doc in docs])


for i in range(len(os.listdir("prompts")), numb + len(os.listdir("prompts"))):
    retriever = DirectoryLoader("prompts")

    llm = ChatOpenAI(model="gpt-4o")

    chain = (prompt | llm | StrOutputParser())

    result = chain.invoke(
        input={
            "previous_prompts": docs_to_prompts(retriever.load()),
            "prompt": "You are an AI bot that knows everything about cats. I will send you questions about cats, and you should answer those questions to the best of your ability."
        }
    )

    open("prompts/prompt_{}.txt".format(i), "w").write(result)
