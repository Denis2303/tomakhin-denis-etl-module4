import json
import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(44)

output_path = Path('data/raw/kafka_loan_events.jsonl')
target_mb = float(os.environ.get('TARGET_MB', '25'))
target_bytes = int(target_mb * 1024 * 1024)
output_path.parent.mkdir(parents=True, exist_ok=True)

regions = ['DE-HE', 'DE-BE', 'DE-BY', 'DE-HH', 'DE-NW', 'DE-SN', 'DE-ST', 'DE-TH']
risk_levels = ['low', 'medium', 'high']
decisions = ['approved', 'rejected', 'manual_review']
doc_types = ['passport', 'income_statement', 'employment_contract', 'bank_statement']
doc_statuses = ['verified', 'rejected', 'pending']
start_dt = datetime(2026, 5, 1, 0, 0, 0, tzinfo=timezone.utc)

i = 1
with output_path.open('w', encoding='utf-8') as file:
    while file.tell() < target_bytes:
        score = random.randint(300, 850)
        risk_level = 'low' if score >= 700 else 'medium' if score >= 560 else 'high'
        event_time = start_dt + timedelta(seconds=random.randint(0, 60 * 60 * 24 * 45))
        documents = []
        for _ in range(random.randint(1, 3)):
            documents.append({
                'type': random.choice(doc_types),
                'status': random.choice(doc_statuses)
            })
        event = {
            'application_id': f'loan_{i:09d}',
            'customer': {
                'customer_id': f'cust_{random.randint(10000, 999999)}',
                'region': random.choice(regions)
            },
            'loan': {
                'amount': random.randrange(1000, 80000, 500),
                'term_months': random.choice([6, 12, 18, 24, 36, 48, 60])
            },
            'scoring': {
                'score': score,
                'risk_level': risk_level
            },
            'documents': documents,
            'decision_status': random.choice(decisions),
            'submitted_at': event_time.isoformat().replace('+00:00', 'Z')
        }
        file.write(json.dumps(event, ensure_ascii=False) + '\n')
        i += 1
        if i % 10000 == 0:
            file.flush()

print(output_path)
print(round(output_path.stat().st_size / 1024 / 1024, 2))
