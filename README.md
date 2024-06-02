# Prompt Defender
![PyPI](https://img.shields.io/pypi/v/prompt-defender)

Read the documentation at [Prompt Defender - Docs](https://promptshield.readme.io/docs)

## Installation

```pip install prompt-defender```

## Quick start

```python
from prompt_defender import CompositeWallExecutorBuilder, build_drawbridge, remote_keep_builder, build_xml_scanner, build_remote_wall_executor, build_prompt_validator, Defence

if __name__ == "__main__":
  compose_wall = CompositeWallExecutorBuilder()
  compose_wall.add_wall_executor(build_xml_scanner)
  compose_wall.add_wall_executor(build_remote_wall_executor(fast_check=True))
  compose_wall.add_wall_executor(build_prompt_validator())

  defence = Defence(
    wall=compose_wall.build(),
    keep=remote_keep_builder(),
    drawbridge=build_drawbridge(allow_unsafe_scripts=True)
  )

  prepared_prompt = defence.prepare_prompt("Your job is to answer user questions about cats {user_question}")

  print(defence.check_user_input("What is the best cat? " + prepared_prompt.safe_prompt))

  print(defence.check_prompt_output("This should all be okay "))

```

## Wall

Wall is a part of the Prompt Defender project that is responsible for validating prompts. It uses a combination of
local and remote checks to ensure the safety and validity of the prompts. The main component of the Wall is
the `create_wall` function, which orchestrates the execution of the different validation checks.

The `create_wall` function is responsible for creating an instance of the ValidatorExecutor class,
which is used to validate prompts. There are two types of validation checks that can be performed: local and remote (
these are both used from the same wall instance, depending on the parameters passed)

The remote instance uses [Prompt Defender - Docs](https://promptshield.readme.io/docs) to validate prompts. This is the
most
useful and powerful part of the Wall, as it allows you to perform complex validation checks on prompts, in particular
checking for jailbreak attacks. To use the remote instance, you'll need to retrieve a valid API key which you
can get at [Prompt Defender](https://defender.safetorun.com/).

The local instance is used to perform simple validation checks on prompts. This is useful for checking that the prompt
meets certain constraints - ensuring your [instruction defence](https://promptshield.readme.io/docs/building-your-keep),
and is powerful when combined with the remote instance to provide a comprehensive validation. Here's a brief description
of how to use the create_wall function:

Parameters:

**PromptDefender Remote values**

* allow_pii - Whether to allow PII in the prompt. If this is set to 'false', the prompt - will be rejected if it
  contains PII. (Note: to use this, you'll either need to pass in a valid API key or set the PROMPT_DEFENDER_API_KEY
  environment and remote_jailbreak_check to true)
* api_key - The API key to use for the remote wall checker
* user_id - The user ID to use for the remote wall checker
* session_id - The session ID to use for the remote wall checker

**PromptDefender Local values**

* max_prompt_length - The maximum length of a prompt
* allowed_prompt_values - A list of allowed prompt values
* xml_tag - The XML tag to scan for in the prompt. If this is set, the prompt will be rejected if it contains
  the specified tag. This is useful when you are using a prompt with instruction defence,
  see [Prompt Defender - Keep](https://promptshield.readme.io/docs/building-your-keep) for more information on
  instruction defence

## Drawbridge

Drawbridge is a part of the Prompt Defender project that is responsible for validating the response of an LLM execution.
That is - after you have executed an LLM, you can use Drawbridge to check the response for any potential security
issues.

The Drawbridge class in the drawbridge.py file is used to validate the response of an LLM execution. It has two main
functionalities:

* Checking for a canary in the response.

* Cleaning the response by removing scripts if allow_unsafe_scripts is set to False.
  Here is a basic usage example:

```python
from drawbridge import build_drawbridge

# Create a Drawbridge instance
drawbridge = build_drawbridge(canary="test_canary", allow_unsafe_scripts=False)

# Validate and clean a response
response = "<script>alert('Hello!');</script>test_canary"
response_ok, cleaned_response = drawbridge.validate_response_and_clean(response)

print(f"Response OK: {response_ok}")
print(f"Cleaned Response: {cleaned_response}")
```

In this example, we first import the `build_drawbridge` function from the drawbridge module. We then use this function
to
create a Drawbridge instance, specifying a canary string that we want to check for in the response.

Next, we have a response string that we want to validate and clean. We pass this response to the
validate_response_and_clean method of our Drawbridge instance. This method returns two values:

* response_ok: This is a boolean value that indicates whether the canary was found in the response.
* cleaned_response: This is the cleaned version of the response. If allow_unsafe_scripts is False (which is the
  default),
  any scripts in the response will be removed.
