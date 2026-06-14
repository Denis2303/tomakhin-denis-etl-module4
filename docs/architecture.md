# Архитектура решения

## Общая схема

```text
                    ┌────────────────────┐
                    │ Python generators  │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
transactions_v2.csv    applications.csv     kafka_loan_events.jsonl
        │                     │                     │
        ▼                     ▼                     ▼
      YDB             Object Storage              Kafka
        │                     │                     │
        ▼                     ▼                     ▼
 Data Transfer      Data Processing          Data Processing
        │              PySpark job             PySpark job
        ▼                     │                     │
 Object Storage              ▼                     ▼
                      Object Storage          Object Storage
                              │                     │
                              └─────────┬───────────┘
                                        ▼
                                    DataLens
```

## Задание 1

Источник данных: YDB table `transactions_v2`.

Назначение: Object Storage.

Механизм переноса: Yandex Data Transfer.

## Задание 2

Источник данных: CSV-файл в Object Storage.

Вычисления: PySpark job в Yandex Data Processing.

Оркестрация: Apache Airflow DAG.

Результат: parquet-таблицы в Object Storage.

## Задание 3

Источник данных: Kafka topic `loan-applications`.

Формат сообщений: JSON.

Вычисления: PySpark job в Yandex Data Processing.

Результат: плоская parquet-таблица и агрегированная parquet-витрина.

## Задание 4

Источник данных: агрегированные результаты обработки.

Визуализация: Yandex DataLens dashboard.
