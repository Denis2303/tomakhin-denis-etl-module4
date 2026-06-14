from pathlib import Path

files = [
    Path('data/raw/transactions_v2.csv'),
    Path('data/raw/applications.csv'),
    Path('data/raw/kafka_loan_events.jsonl')
]

for path in files:
    if path.exists():
        print(path, round(path.stat().st_size / 1024 / 1024, 2), 'MB')
    else:
        print(path, 'not found')
