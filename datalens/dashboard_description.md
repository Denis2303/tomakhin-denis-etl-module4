# Описание DataLens dashboard

## Название

```text
ETL Exam Dashboard
```

## Источники данных

Для визуализации используются результаты PySpark-обработки:

```text
s3://etl-exam-denis-2026/output/applications/applications_daily_summary
s3://etl-exam-denis-2026/output/applications/applications_monthly_summary
s3://etl-exam-denis-2026/output/kafka/kafka_events_summary
```

Если DataLens не подключается напрямую к parquet в Object Storage, можно выгрузить агрегаты в CSV и загрузить их как файловый источник.

## Поля applications_daily_summary

```text
event_date
region_code
product_type
risk_level
decision_status
applications_count
requested_amount_sum
approved_amount_sum
avg_credit_score
avg_processing_time_sec
avg_approval_rate_amount
```

## Поля applications_monthly_summary

```text
event_month
region_code
product_type
applications_count
approved_count
rejected_count
manual_review_count
requested_amount_sum
approved_amount_sum
avg_credit_score
```

## Поля kafka_events_summary

```text
region_code
risk_level
decision_status
count
```

## Рекомендуемые чарты

### 1. Количество заявок по дням

Dataset: `applications_daily_summary`

Тип: line chart

- X: `event_date`
- Y: `SUM(applications_count)`
- Color: `decision_status`

### 2. Количество заявок по регионам

Dataset: `applications_daily_summary`

Тип: bar chart

- X: `region_code`
- Y: `SUM(applications_count)`
- Color: `risk_level`

### 3. Статусы решений

Dataset: `applications_daily_summary`

Тип: pie chart или donut chart

- Dimension: `decision_status`
- Measure: `SUM(applications_count)`

### 4. Средний credit score

Dataset: `applications_daily_summary`

Тип: bar chart

- X: `risk_level`
- Y: `AVG(avg_credit_score)`

### 5. Суммы заявок и одобрений

Dataset: `applications_monthly_summary`

Тип: bar chart

- X: `product_type`
- Y1: `SUM(requested_amount_sum)`
- Y2: `SUM(approved_amount_sum)`

### 6. Kafka summary

Dataset: `kafka_events_summary`

Тип: table

- `region_code`
- `risk_level`
- `decision_status`
- `count`

## Фильтры dashboard

Добавить селекторы:

```text
region_code
product_type
risk_level
decision_status
event_date
```

## Что вставить в отчёт

1. Скриншот списка datasets.
2. Скриншот нескольких charts.
3. Скриншот dashboard целиком.
4. Ссылку на dashboard, если она доступна.
