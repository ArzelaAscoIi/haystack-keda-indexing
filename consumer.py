from pathlib import Path
from time import sleep
from typing import List

import structlog

from aws_service import AWSService
from config import LOCAL_DOWNLOAD_DIR, S3_BUCKET, SQS_QUEUE
from pipeline import get_pipeline

# To learn more about logging in python check out my other article
# about structolg! https://medium.com/@ArzelaAscoli/writing-professional-python-logs-e1f31635b60b
logger = structlog.get_logger(__name__)

# Initialize AWS service
aws_service = AWSService(SQS_QUEUE, S3_BUCKET, LOCAL_DOWNLOAD_DIR)

# load pipeline
pipeline = get_pipeline("./pipelines/pipeline.yaml")

while True:
    # fetch files from aws
    files: List[Path] = aws_service.get_files()
    if not files:
        logger.info("No files to process")
        sleep(5)
        continue

    # process files if found
    logger.info("Found files", files=files)

    # run indexing for downloaded files
    documents = pipeline.run(file_paths=files)
    logger.info("Processed files", documents=documents)
