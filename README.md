# DataFlow — Large-Scale Multi-Source Data Ingestion Pipeline

Extensible ingestion framework for heterogeneous sources with schema-on-read normalization, idempotency, streaming fan-out, data-quality gates, source health analytics, and AWS integration adapters.

## Architecture
Sources → connector pool → validation/normalization → Redis SETNX dedup → Redis Streams → SQS → Lambda → S3/DynamoDB.

## Features
- `SourceConnector` abstraction with REST, CSV/JSON, MQTT and database connector boundaries
- asyncio connector pool
- schema-on-read normalization
- Redis SETNX-compatible idempotency layer
- Redis Streams consumer-group architecture
- SQS backpressure boundary
- S3 raw/normalized archive adapter
- DynamoDB source metrics adapter
- CloudWatch custom metrics adapter
- freshness/value validation and quarantine
- rolling ±2σ source anomaly detection
- Python + Java components
- Docker and GitHub Actions
- normalization benchmark harness

## Run
```bash
docker compose up -d redis postgres
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r python/requirements.txt
PYTHONPATH=python python -m dataflow.demo
```

Benchmark:
```bash
PYTHONPATH=python python benchmark/benchmark_normalization.py --records 10000
```

The benchmark reports measured throughput. The resume's 4.2x parsing and 2.9x end-to-end improvements are not fabricated or embedded as guaranteed results; reproduce them on the target workload before claiming them.
