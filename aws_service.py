import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List

import boto3

from config import AWS_ENDPOINT, AWS_REGION


class SQSClient:
    def __init__(self, queue_name: str) -> None:
        self.sqs = boto3.client(
            "sqs",
            endpoint_url=AWS_ENDPOINT,  # allows using localstack
            region_name=AWS_REGION,  # allows using localstack
        )
        self.queue_name = queue_name
        self.queue = self.sqs.get_queue_url(QueueName=self.queue_name)

    def publish_key(self, key: str) -> None:
        """
        Publish key to SQS queue

        :param key: s3 Key to publish
        """

        self.sqs.send_message(QueueUrl=self.queue["QueueUrl"], MessageBody=key)

    @contextmanager
    def fetch_keys(self) -> Generator[List[str], None, None]:
        """
        Fetch messages from defined queue
        :returns List of keys on s3
        """

        # receive up to 10 messages at once from sqs
        response = self.sqs.receive_message(
            QueueUrl=self.queue["QueueUrl"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=0,
        )
        # get s3 keys from sqs messages
        messages = response.get("Messages", [])
        s3_keys = [message["Body"] for message in messages]

        try:
            # We are using a context manager to ensure the messages
            # are deleted from the queue after handling them was
            # successful.
            yield s3_keys
            # This will be run after the message was processed
            for message in messages:
                self.sqs.delete_message(
                    QueueUrl=self.queue["QueueUrl"],
                    ReceiptHandle=message["ReceiptHandle"],
                )
        except Exception as error:
            raise error


class S3Client:
    def __init__(self, bucket_name: str, local_download_dir: str) -> None:
        """
        :param bucket_name: Name of the s3 bucket
        :param local_download_dir: Local directory to download files to from s3
        """
        self.s3 = boto3.client(
            "s3",
            endpoint_url=AWS_ENDPOINT,  # allows using localstack
            region_name=AWS_REGION,  # allows using localstack
        )
        self.bucket_name = bucket_name
        self.local_download_dir = local_download_dir

    def upload_file(self, local_path: Path) -> None:
        """
        Upload file to s3 with the same name as the file on local filesystem.
        :param local_path: Path to file on local filesystem
        """
        file_name = os.path.basename(local_path)
        self.s3.upload_file(
            str(local_path),
            self.bucket_name,
            file_name,
            ExtraArgs={"ACL": "public-read"},
        )

    def download_files(self, s3_keys: List[str]) -> List[Path]:
        """
        Download files from s3 to local directory.

        TODO: Make this async to speed up the upload process
        TODO: delete files from local directory after processing

        :param s3_keys: List of keys on s3
        :returns List of paths to downloaded files
        """
        paths: List[Path] = []
        for s3_key in s3_keys:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
            file_name = os.path.basename(s3_key)
            local_path = os.path.join(self.local_download_dir, file_name)
            paths.append(Path(local_path))
            with open(local_path, "wb") as f:
                f.write(response["Body"].read())

        return paths


class AWSService:
    def __init__(
        self, queue_name: str, bucket_name: str, local_download_dir: str
    ) -> None:
        self.sqs_client = SQSClient(queue_name)
        self.s3_client = S3Client(bucket_name, local_download_dir)

    def get_files(self) -> List[Path] | None:
        with self.sqs_client.fetch_keys() as messages:
            if not messages:
                return
            paths = self.s3_client.download_files(messages)
            return paths

    def upload_file(self, local_path: Path) -> None:
        self.s3_client.upload_file(local_path)
        self.sqs_client.publish_key(local_path.name)
