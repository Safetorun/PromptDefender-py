# Prompt Defender

## Installation

```pip install prompt-defender```

## Wall

Wall is a part of the Prompt Defender project that is responsible for validating prompts. It uses a combination of
local and remote checks to ensure the safety and validity of the prompts. The main component of the Wall is
the `create_wall` function, which orchestrates the execution of the different validation checks.

The `create_wall` function is responsible for creating an instance of the ValidatorExecutor class,
which is used to validate prompts. There are two types of validation checks that can be performed: local and remote (
these are both used from the same wall instance, depending on the parameters passed)

The remote instance uses [Prompt Defender - Docs](https://promptshield.readme.io/docs) to validate prompts. This is the most
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