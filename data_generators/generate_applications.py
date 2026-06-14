import csv
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(43)

output_path = Path('data/raw/applications.csv')
target_mb = float(os.environ.get('TARGET_MB', '60'))
target_bytes = int(target_mb * 1024 * 1024)
output_path.parent.mkdir(parents=True, exist_ok=True)

regions = ['DE-HE', 'DE-BE', 'DE-BY', 'DE-HH', 'DE-NW', 'DE-SN', 'DE-ST', 'DE-TH']
products = ['cash_loan', 'credit_card', 'mortgage', 'car_loan', 'bnpl']
risk_levels = ['low', 'medium', 'high']
decisions = ['approved', 'rejected', 'manual_review']
channels = ['mobile', 'web', 'office', 'partner_api']
start_dt = datetime(2026, 5, 1, 0, 0, 0)

with output_path.open('w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'application_id',
        'event_time',
        'customer_id',
        'region_code',
        'product_type',
        'requested_amount',
        'term_months',
        'credit_score',
        'risk_level',
        'decision_status',
        'approved_amount',
        'channel',
        'employee_review_flag',
        'processing_time_sec'
    ])
    i = 1
    while file.tell() < target_bytes:
        event_time = start_dt + timedelta(seconds=random.randint(0, 60 * 60 * 24 * 45))
        requested_amount = random.randrange(1000, 80000, 500)
        credit_score = random.randint(300, 850)
        risk_level = 'low' if credit_score >= 700 else 'medium' if credit_score >= 560 else 'high'
        decision_status = random.choices(decisions, weights=[55, 25, 20], k=1)[0]
        approved_amount = requested_amount if decision_status == 'approved' else 0
        if decision_status == 'manual_review':
            approved_amount = int(requested_amount * random.uniform(0.3, 0.8))
        writer.writerow([
            f'app_202605_{i:09d}',
            event_time.strftime('%Y-%m-%d %H:%M:%S'),
            f'cust_{random.randint(10000, 999999)}',
            random.choice(regions),
            random.choice(products),
            requested_amount,
            random.choice([6, 12, 18, 24, 36, 48, 60]),
            credit_score,
            risk_level,
            decision_status,
            approved_amount,
            random.choice(channels),
            str(decision_status == 'manual_review').lower(),
            random.randint(3, 600)
        ])
        i += 1
        if i % 10000 == 0:
            file.flush()

print(output_path)
print(round(output_path.stat().st_size / 1024 / 1024, 2))
