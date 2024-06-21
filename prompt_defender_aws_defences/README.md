# README

## Prompt Defender AWS Defences Library

Welcome to the **Prompt Defender AWS Defences** library. This library is designed to help you defend against prompt injection attacks by leveraging AWS services such as AWS Comprehend and SageMaker. The library is written in Python and can be easily installed via pip.

### Installation

You can install the library using pip:

```bash
pip install prompt-defender-aws-defences
```

### Usage

This library provides two main classes to help in detecting and preventing prompt injection attacks:

1. **AwsPIIScannerWallExecutor**: This class uses AWS Comprehend to scan text for Personally Identifiable Information (PII).
2. **SagemakerWallExecutor**: This class calls a remote SageMaker endpoint to validate the prompt.

#### Example

You can find example usage in the `example.py` file.

```python
from prompt_defender_aws_defences import AwsPIIScannerWallExecutor, SagemakerWallExecutor

# Example usage of AwsPIIScannerWallExecutor
pii_executor = AwsPIIScannerWallExecutor()
validation_result = pii_executor.is_user_input_safe("Your text to scan here")
print(validation_result)

# Example usage of SagemakerWallExecutor
sagemaker_executor = SagemakerWallExecutor(sagemaker_name="your-sagemaker-endpoint")
validation_result = sagemaker_executor.is_user_input_safe("Your text to validate here")
print(validation_result)
```

### Directory Structure

The main class files are located in the `prompt_defender_aws_defences` directory:

- `prompt_defender_aws_defences/__init__.py`: Initializes the package and imports the main executors.
- `prompt_defender_aws_defences/wall/pii_detection.py`: Contains the `AwsPIIScanner` and `AwsPIIScannerWallExecutor` classes.
- `prompt_defender_aws_defences/wall/sagemaker_inference.py`: Contains the `RemoteSagemakerCaller` and `SagemakerWallExecutor` classes.
- `prompt_defender_aws_defences/wall/shared.py`: Defines shared utilities such as `MatchLevel` and `match_level_for_score`.
- `prompt_defender_aws_defences/wall/__init__.py`: Initializes the wall module and imports the necessary executors.

### License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for more details.

### Contact

For any questions or issues, please contact the project owner at [admin@safetorun.com](mailto:admin@safetorun.com).

### Contributing

Contributions are welcome! Please refer to the project's [GitHub Issues page](https://github.com/safetorun/PromptDefender-py/issues) for any open issues or feature requests.

### Additional Information

For more details, please visit the project's [Homepage](https://github.com/safetorun/PromptDefender-py).

We hope you find this library useful in defending against prompt injection attacks!

---

Happy coding! 🛡️
