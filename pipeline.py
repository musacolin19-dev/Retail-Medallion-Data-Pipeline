import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = ('order_id', 'day', 'store', 'quantity', 'unit_price')

def transform(rows):
    bronze, silver, quarantine, seen = [], [], [], set()
    for row in rows:
        row = dict(row)
        bronze.append(row)
        try:
            if any(not row.get(k) for k in REQUIRED):
                raise ValueError('missing required column')
            qty = int(row['quantity'])
            price = Decimal(row['unit_price'])
            if qty <= 0 or price < 0:
                raise ValueError('invalid quantity or price')
            if row['order_id'] in seen:
                raise ValueError('duplicate order_id')
            seen.add(row['order_id'])
            silver.append({'order_id': row['order_id'], 'day': row['day'],
                           'store': row['store'], 'quantity': qty,
                           'revenue': str(qty * price)})
        except (ValueError, InvalidOperation, KeyError) as exc:
            quarantine.append({'record': row, 'reason': str(exc)})
    totals = defaultdict(Decimal)
    for item in silver:
        totals[(item['day'], item['store'])] += Decimal(item['revenue'])
    gold = [{'day': day, 'store': store, 'revenue': str(amount)}
            for (day, store), amount in sorted(totals.items())]
    return bronze, silver, gold, quarantine

def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(x) + '\n' for x in records), encoding='utf-8')

def run(input_file, output_dir):
    with Path(input_file).open(newline='', encoding='utf-8') as source:
        layers = transform(csv.DictReader(source))
    for layer, records in zip(('bronze', 'silver', 'gold', 'quarantine'), layers):
        write_jsonl(Path(output_dir) / f'{layer}.jsonl', records)
    return {name: len(items) for name, items in zip(('bronze','silver','gold','quarantine'), layers)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='output')
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), indent=2))
