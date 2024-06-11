import sys

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PythonLoader, UnstructuredMarkdownLoader
import os

template = """I will provide you with a list of files which forms a directory, please generate
a README file for the directory.

Key information to know:

* Examples will be in example.py
* The project owner can be contacted at admin@safetorun.com
* The project is licensed under the Apache license
* The project is written in Python
* The project is a library and can be installed via pip
* The actual class files are inside the {project_name} directory

{context}

"""


def format_docs(docs: list[dict]):
    return "\n\n".join(["{0}:\n\n{1}".format(d.metadata["source"], d.page_content) for d in docs])


prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o")

if __name__ == "__main__":

    project_name = sys.argv[1]

    os.chdir(project_name)

    retriever = DirectoryLoader(project_name, glob="*.py", loader_cls=PythonLoader,
                                recursive=True).load()

    docs = []
    for doc in retriever:
        docs.append(doc)

    retriever = DirectoryLoader(project_name, glob="README.md", recursive=True,
                                loader_cls=UnstructuredMarkdownLoader).load()
    for doc in retriever:
        docs.append(doc)

    if os.path.exists("pyproject.toml"):
        doc_loader = TextLoader("pyproject.toml").load()

        for doc in doc_loader:
            docs.append(doc)

    chain = (
            prompt
            | llm
            | StrOutputParser()
    )

    result = chain.invoke(input={"project_name": project_name, "context": format_docs(docs)})

    open("README.md", "w").write(result)
    os.chdir("..")
