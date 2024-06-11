# README

# Prompt Defender Library

Welcome to the **Prompt Defender** library, a Python package designed to help you defend against prompt injection attacks. This library provides a robust framework for generating safe prompts and validating user inputs to ensure the security of your applications.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Examples](#examples)
- [Modules](#modules)
  - [Defence](#defence)
  - [Keep](#keep)
  - [Wall](#wall)
  - [Drawbridge](#drawbridge)
- [Testing](#testing)
- [License](#license)
- [Contact](#contact)

## Installation

You can install the library using pip:

```bash
pip install prompt-defender
```

## Usage

The Prompt Defender library is designed to be easy to integrate into your Python applications. Below is an example of how to use the library:

### Examples

The `example.py` file contains several examples demonstrating how to use the library. Here is a simple example to get you started:

```python
from prompt_defender import Defence, build_drawbridge, build_xml_scanner, build_prompt_validator

# Configure the defence mechanisms
defence = Defence(
  wall=[
    build_xml_scanner(),
    build_prompt_validator(max_length=100)
  ],
  keep=None,
  drawbridge=build_drawbridge(allow_unsafe_scripts=False)
)

# Prepare a prompt
safe_prompt_response = defence.prepare_prompt("Your job is to answer user questions about cats {user_question}", False)

# Check user input
is_safe, cleaned_instruction = defence.is_user_input_safe("What is the best cat? " + safe_prompt_response.safe_prompt)

# Check prompt output
output_response = defence.check_prompt_output("The best cat is a Maine Coon.")
print(f"Output is safe: {output_response.is_safe}, Cleaned response: {output_response.cleaned_response}")
```

For more detailed examples, please refer to the `example.py` file.

## Modules

### Defence

The `Defence` class integrates several defensive mechanisms against potential prompt injection and jailbreak attempts.

### Keep

The `Keep` module is responsible for generating safe prompts and includes the `RemoteKeepExecutor` class for interacting with remote services.

### Wall

The `Wall` module contains various validators for checking user input and includes classes such as `PromptValidator`, `BasicXmlScanner`, and `PromptDefenderClient`.

### Drawbridge

The `Drawbridge` module provides mechanisms for validating and cleaning the responses of a language model, including the `DefaultDrawbridgeExecutor` class.

## Testing

Unit tests are included in the `tests` directory. You can run the tests using `unittest`:

```bash
python -m unittest discover -s prompt_defender/tests
```

## License

This project is licensed under the Apache License. See the LICENSE file for more details.

## Contact

For any questions, issues, or contributions, please contact the project owner at [admin@safetorun.com](mailto:admin@safetorun.com).

---

Thank you for using Prompt Defender! Together, we can create safer applications.