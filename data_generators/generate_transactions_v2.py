import csv
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

output_path = Path('data/raw/transactions_v2.csv')
target_mb = float(os.environ.get('TARGET_MB', '35'))
target_bytes = int(target_mb * 1024 * 1024)
output_path.parent.mkdir(parents=True, exist_ok=True)

regions = ['DE-HE', 'DE-BE', 'DE-BY', 'DE-HH', 'DE-NW', 'DE-SN', 'DE-ST', 'DE-TH']
campaigns = ['credit_card_offer', 'cash_loan', 'mortgage', 'car_loan', 'deposit', 'insurance']
statuses = ['answered', 'missed', 'busy', 'failed']
responses = ['interested', 'not_interested', 'callback', 'no_answer', 'wrong_number']
start_dt = datetime(2026, 5, 1, 8, 0, 0)

with output_path.open('w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'call_id',
        'call_time',
        'client_id',
        'region_code',
        'campaign_type',
        'call_status',
        'client_response',
        'duration_sec',
        'follow_up_required'
    ])
    i = 1
    while file.tell() < target_bytes:
        call_time = start_dt + timedelta(seconds=random.randint(0, 60 * 60 * 24 * 45))
        call_status = random.choices(statuses, weights=[72, 15, 8, 5], k=1)[0]
        client_response = random.choice(responses) if call_status == 'answered' else 'no_answer'
        duration = random.randint(20, 900) if call_status == 'answered' else random.randint(0, 25)
        follow_up = client_response in ['interested', 'callback']
        writer.writerow([
            f'call_202605_{i:09d}',
            call_time.strftime('%Y-%m-%d %H:%M:%S'),
            f'client_{random.randint(1000, 999999)}',
            random.choice(regions),
            random.choice(campaigns),
            call_status,
            client_response,
            duration,
            str(follow_up).lower()
        ])
        i += 1
        if i % 10000 == 0:
            file.flush()

print(output_path)
print(round(output_path.stat().st_size / 1024 / 1024, 2))
