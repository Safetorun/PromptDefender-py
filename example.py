from wall import should_block_prompt
from wall import create_wall

wall = create_wall(
    # These options first require you to have a Prompt Defender account which you can sign up for at
    # https://defender.safetorun.com. Once you have an account you can get an API key  to use with the wall.
    remote_jailbreak_check=True,
    api_key="your_api_key_here",  # Get this from https://defender.safetorun.com
    rapid_api_key="your_api_key_here",  # Get this from https://rapidapi.com/promptdefender-promptdefender-default/api/prompt-defender
    user_id="test_user",
    session_id="test_session",
    allow_pii=False,

    # When you create a prompt, with Prompt Defender - Keep, you will get
    # an XML tag that wraps user input. Pass this tag to the remote endpoint
    # in order to check for potential XML escaping which is likely because
    # someone is trying to attack your system
    xml_tag="tag",

    # The following are used for prompt validation - if you are only
    # expecting a certain number of values, or a certain length of prompt
    # you can use these to enforce that.

    max_prompt_length=100,
    allowed_prompt_values=["hello", "world"]
)

validation_response = wall.validate_prompt("hello")

if validation_response.contains_pii:
    print("Prompt contains PII")
elif validation_response.suspicious_user:  # etc etc etc
    print("Prompt is suspicious")
elif should_block_prompt(validation_response):
    print("Prompt should be blocked")
else:
    print("Prompt is OK")
