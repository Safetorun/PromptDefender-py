import os
import sys

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PythonLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

template = """
I will provide you with a list of python code, including tests. I will also provide you with a class which I want you 
to generate a test file for. When generating tests, use the provided code as a reference 
and try to keep in mind the style and structure of the existing tests.

Here is the code:

<code>
{context}
</code>

Class to test: {class_to_test}
File in which we will store the class: {test_class}

Now, generate a unit test for the class {class_to_test} using the provided code as a reference. 

* This code will be written directly to file, so include all necessary imports and setup.
* This code should be a complete unit test for the class {class_to_test}.
* This code should be written in Python.
* This code will be written directly to file, so only return code - do not return any extra information, no ```python or ``` at all
* Consider the file in which we will story the class, make sure that your imports are relative to that file.
"""


def format_docs(docs: list[dict]):
    return "\n\n".join(["{0}:\n\n{1}".format(d.metadata["source"], d.page_content) for d in docs])


prompt = PromptTemplate.from_template(template)
llm = ChatGoogleGenerativeAI(model="gemini-pro")


def generate_tests(class_to_test, test_class):
    retriever = DirectoryLoader(".", glob="*.py", loader_cls=PythonLoader,
                                recursive=True, show_progress=True).load()

    docs = []
    for doc in retriever:
        if "venv" in doc.metadata["source"]:
            continue
        docs.append(doc)

    chain = (
            prompt
            | llm
            | StrOutputParser()
    )

    print("Generating tests for class: ", class_to_test)
    open("all_files.txt", "w").write(format_docs(docs))

    result = chain.invoke(
        input={"test_class": test_class,
               "class_to_test": class_to_test,
               "context": format_docs(docs)
               }
    )

    open(test_class, "w").write(result.removeprefix("```python\n").removesuffix("\n```"))


if __name__ == "__main__":
    class_to_test = sys.argv[1]
    test_class = sys.argv[2]
    generate_tests(class_to_test, test_class)
