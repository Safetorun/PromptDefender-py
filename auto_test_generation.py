import argparse
import os
import unittest
import yaml
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PythonLoader
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

fix_tests = """
    I am going to provide you with a test file. I want you to fix the test file so that it passes.
    
    First, I will give you all files in the directory. I will then provide you with the test file which is broke.
    I will also provide you with the errors and failures from the test run.
    
    Your task is to fix the test file so that it passes. You can make any changes you want to the test file.
    Return only the test file, and it will replace all existing contents of the file - so ensure you include everything,
    including imports and setup.
    
    * For imports prefer using import . or import .., e.g. import ..wall is preferrable to import prompt_defender.wall
    * This code will be written directly to file, so include all necessary imports and setup.
    * This code should be written in Python.
    * This code will be written directly to file, so only return code - do not return any extra information, no ```python or ``` at all
    * Consider the file in which we will store the class, make sure that your imports are relative to that file.
    * If the imports are already correct in the broken test, use those as inspiration. E.g. if the broken test uses . or .. 

    Your response will be pasted entirely into a .py file, so ensure it runs.
    
    Here are the files:
        <files>{files}</files>
        
    Here is the broken test:
        <broken_test>{broken_test}</broken_test>
    
    Here are the errors:
        <errors>{errors}</errors>
    
    Here are the failures:
        <failures>{failures}</failures>
        
    File location:
        {test_file}
    
    
"""

missing_tests_finder = """
    I will provide you with a list of python code, including tests. Please return a json object, with an array called 
    missing_tests which contains the names of all classes which do not have a corresponding test file. In this json
    array, please include the names of tests which you think could be improved - for example if they don't sufficiently
    cover the test cases.
    
    Exclusion:
        * Exclude any files which are clearly __init__ or test classes
        * Exclude any files that are in the ignored files list below
        
    {ignored_files}
    
    Example response:
    'missing_tests': ["full/path/to/file.py", "full/path/to/another_file.py"],
    "tests_to_improve": ["full/path/to/test_file.py"]
    
    
    Here are the files:
    
    <files>
        {docs}
    </files>
"""

test_generate_prompt = """
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
* Consider the file in which we will store the class, make sure that your imports are relative to that file.
"""


def format_docs(docs: list[dict]):
    return "\n\n".join(["{0}:\n\n{1}".format(d.metadata["source"], d.page_content) for d in docs])


llm = ChatOpenAI(model="gpt-4o")


def generate_tests(class_to_test: str, test_class: str):
    docs = get_all_python_files()
    prompt = PromptTemplate.from_template(test_generate_prompt)
    chain = (
            prompt
            | llm
            | StrOutputParser()
    )

    result = chain.invoke(
        input={"test_class": test_class,
               "class_to_test": class_to_test,
               "context": docs
               }
    )

    open(test_class, "w").write(result.removeprefix("```python\n").removesuffix("\n```"))


def get_all_python_files() -> str:
    retriever = DirectoryLoader(".", glob="*.py", loader_cls=PythonLoader,
                                recursive=True, show_progress=True).load()
    docs = []
    for doc in retriever:
        if "venv" in doc.metadata["source"]:
            continue
        docs.append(doc)

    return format_docs(docs)


def run_tests(test_class: str) -> (bool, list, list):
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(test_class), pattern=os.path.basename(test_class))

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    return result.wasSuccessful(), result.errors, result.failures


def perform_action(success, errors, failures, test_file):
    if success:
        print("Test passed. You're good to go!")
    else:
        print("Test failed. Performing failure action...")
        print("Errors: ", errors)
        print("Failures: ", failures)

        docs = get_all_python_files()
        prompt = PromptTemplate.from_template(fix_tests)
        chain = (
                prompt
                | llm
                | StrOutputParser()
        )

        result = chain.invoke(
            input={"files": docs, "test_file": test_file, "broken_test": open(test_file, "r").read(), "errors": errors,
                   "failures": failures}
        )

        open(test_file, "w").write(result.removeprefix("```python\n").removesuffix("\n```"))


def find_missing_tests(ignored_files: list[str]):
    """ Find missing tests in the codebase."""

    print("Finding missing tests...")
    print("Going to ignore the following files: ", ignored_files)
    docs = get_all_python_files()
    prompt = PromptTemplate.from_template(missing_tests_finder)

    chain = (
            prompt
            | llm
            | JsonOutputParser()
    )

    result = chain.invoke(
        input={"docs": docs, "ignored_files": "\n".join(ignored_files)}
    )

    print(result)
    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate tests based on a configuration file.')
    parser.add_argument('-c', '--config', default='test_generation_config.yaml', help='Path to the configuration file.')

    subparsers = parser.add_subparsers(dest='command')
    missing_tests_parser = subparsers.add_parser('find')
    add_tests_parser = subparsers.add_parser('add')
    fix_parser = subparsers.add_parser('fix')

    add_tests_parser.add_argument('-t', '--test', help='Path to the test file.')
    add_tests_parser.add_argument('-c', '--clazz', help='Class to test.')

    fix_parser.add_argument('-t', '--test', help='Path to the test file.')

    args = parser.parse_args()

    if os.path.exists(args.config):
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
            ignored_files = config['ignore']
    else:
        ignored_files = []

    if args.command == 'find':
        find_missing_tests(ignored_files)
    elif args.command == 'add':
        generate_tests(args.clazz, args.test)
        test_result, errors, failures = run_tests(args.test)
        perform_action(test_result, errors, failures, args.test)
    elif args.command == 'fix':
        test_result, errors, failures = run_tests(args.test)

        while not test_result:
            perform_action(test_result, errors, failures, args.test)
            test_result, errors, failures = run_tests(args.test)

        print("Fixed test result: ", test_result)
