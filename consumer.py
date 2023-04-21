from pathlib import Path
from time import sleep
from typing import List
from config import LOCAL_DIR, S3_BUCKET, SQS_QUEUE
from aws_service import AWSService
import structlog

from pipeline import get_pipeline

# To learn more about logging in python check out my other article
# about structolg! https://medium.com/@ArzelaAscoli/writing-professional-python-logs-e1f31635b60b
logger = structlog.get_logger(__name__)


# Initialize AWS service
aws_service = AWSService(SQS_QUEUE, S3_BUCKET, LOCAL_DIR)

# load pipeline
pipeline = get_pipeline("./pipelines/pipeline.yaml")

while True:
    # fetch files from aws
    files: List[Path] = aws_service.get_files()
    if not files:
        logger.info("No files to upload")
        sleep(5)
        continue

    # process files if found
    logger.info("Found files", files=files)

    # run indexing for downloaded files
    pipeline.run(file_paths=files)
