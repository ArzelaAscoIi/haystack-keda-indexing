from pathlib import Path
from time import sleep
from config import LOCAL_DIR, S3_BUCKET, SQS_QUEUE
from sqs_client import AWSService


aws_service = AWSService(SQS_QUEUE, S3_BUCKET, LOCAL_DIR)
aws_service.upload_file(Path("./test.txt"))
