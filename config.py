import ast
import os

# AWS
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")

SQS_QUEUE = os.getenv("SQS_QUEUE", "test-queue")
S3_BUCKET = os.getenv("SQS_QUEUE", "test-bucket")

# Local
LOCAL_DIR = os.getenv("LOCAL_DIR", "/tmp")
