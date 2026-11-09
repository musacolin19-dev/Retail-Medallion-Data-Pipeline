# Retail Medallion Data Pipeline

A miniature Bronze/Silver/Gold data lake pipeline that turns raw order records into validated transactions and daily business aggregates. Demonstrates idempotent processing, schema validation, deduplication, quarantine of invalid records, and repeatable analytics. It uses the Python standard library so you can run it locally before porting to PySpark or Databricks.

## Quick start

```bash
python pipeline.py --input samples/orders.csv --output output
python -m unittest discover -s tests -v
```

## Architecture and scope

Bronze: preserved raw rows; Silver: validated deduplicated facts; Gold: daily revenue grouped by store. JSONL stands in for Delta/Parquet to keep this starter dependency-free.

**Portfolio note:** Original educational starter code, not a production deployment. Use only synthetic/public datasets, document your own extensions, and test integrations before claiming production experience.
