from pathlib import Path
from time import sleep

from aws_service import AWSService
from config import LOCAL_DIR, S3_BUCKET, SQS_QUEUE

aws_service = AWSService(SQS_QUEUE, S3_BUCKET, LOCAL_DIR)
aws_service.upload_file(Path("./data/test.txt"))
