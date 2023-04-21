#!/usr/bin/env bash

set -euo pipefail

echo "configuring sqs"
echo "==================="
LOCALSTACK_HOST=localhost
AWS_REGION=eu-central-1

create_queue() {
    local QUEUE_NAME_TO_CREATE=$1
    awslocal --endpoint-url=http://${LOCALSTACK_HOST}:4566 sqs create-queue --queue-name ${QUEUE_NAME_TO_CREATE} --region ${AWS_REGION} --attributes VisibilityTimeout=30
}
create_bucket() {
    local BUCKET_NAME_TO_CREATE=$1
    awslocal --endpoint-url=http://${LOCALSTACK_HOST}:4566 s3api create-bucket --bucket ${BUCKET_NAME_TO_CREATE}
}

create_queue "test-queue"
create_bucket "test-bucket"