# Architecture

`SourceConnector` is the extension point. Connector instances are ephemeral; production state belongs in Redis/DynamoDB. Redis Streams consumer groups provide fan-out and SQS can form a durable backpressure boundary before Lambda workers. S3, DynamoDB and CloudWatch adapters keep cloud integration separate from core ingestion logic.
