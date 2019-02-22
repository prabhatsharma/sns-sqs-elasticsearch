# AWS SNS notifications to elasticsearch

## Problem statement
Search via AWS Notifications

## Solution
Push SNS notifications to an elasticsearch cluster and use kibana to search logs.

## Implementation:

Pick any messages that you receive in the Queue sent by SNS and push them to elastic-search

workflow looks like

SNS -> SQS Queue <- container -> elasticsearch

> Make sure that you have a [Dead-Letter-Queue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) to capture events that you are not able to process.

## SQS policy

```json
{
  "Version": "2012-10-17",
  "Id": "from-Concerto-SNS",
  "Statement": [
    {
      "Sid": "concerto",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:6567-my-account:concerto",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:us-east-1:546464sns-sender-account:*"
        }
      }
    }
  ]
}
  ```
