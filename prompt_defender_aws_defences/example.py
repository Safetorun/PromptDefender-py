import os

from prompt_defender_aws_defences import SagemakerWallExecutor, AwsPIIScannerWallExecutor

# Initialize the PiiDetection class
pii_detector = AwsPIIScannerWallExecutor()

# Use the PiiDetection class to check if a string contains PII
text = "My name is John Doe and my email is john.doe@example.com"
contains_pii = pii_detector.is_user_input_safe(text).unacceptable_prompt

if contains_pii:
    print("The text contains PII.")
else:
    print("The text does not contain PII.")

# Initialize the SageMakerInference class
sagemaker_infer = SagemakerWallExecutor(os.getenv("SAGEMAKER_ENDPOINT_NAME"))

# Use the SageMakerInference class to make an inference
input_data = {"instances": [{"features": [1, 2, 3, 4, 5]}]}
response = sagemaker_infer.predict(input_data)

print("The inference response is:", response)
