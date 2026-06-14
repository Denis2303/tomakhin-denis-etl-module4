# Томахин Денис. Итоговое ДЗ. Модуль 4. ETL-процессы

Проект подготовлен для итоговой практической работы по дисциплине «ETL-процессы».

В проекте есть решение для четырёх частей задания:

1. Yandex DataTransfer: перенос таблицы `transactions_v2` из YDB в Object Storage.
2. Yandex Data Processing + Airflow: обработка CSV-файла `applications.csv` через PySpark-задание.
3. Managed Service for Apache Kafka + PySpark: чтение JSON-событий из Kafka, разбор вложенного JSON и сохранение плоской таблицы.
4. DataLens: описание дашборда для визуализации результатов.

## Структура проекта

```text
.
├── data_generators
│   ├── generate_applications.py
│   ├── generate_kafka_events.py
│   └── generate_transactions_v2.py
├── dags
│   └── dataproc_applications_dag.py
├── datalens
│   └── dashboard_description.md
├── docs
│   └── architecture.md
├── kafka
│   └── send_events_to_kafka.py
├── report
│   ├── final_report_template.md
│   └── screenshots_checklist.md
├── scripts
│   └── local_size_check.py
├── spark
│   ├── kafka_flatten.py
│   └── process_applications.py
├── yql
│   ├── check_transactions_v2.yql
│   ├── create_transactions_v2.yql
│   └── sample_transactions_v2.yql
├── FULL_GUIDE.md
├── requirements.txt
└── .env.example
```

## Быстрый локальный запуск генерации данных

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Установка библиотек:

```bash
pip install -r requirements.txt
```

Генерация файлов:

```bash
python data_generators/generate_transactions_v2.py
python data_generators/generate_applications.py
python data_generators/generate_kafka_events.py
python scripts/local_size_check.py
```

После этого появятся файлы:

```text
data/raw/transactions_v2.csv
data/raw/applications.csv
data/raw/kafka_loan_events.jsonl
```

## Что сдавать

В LMS нужно прикрепить ссылку на public GitHub-репозиторий. В репозитории должны быть:

- код проекта;
- YQL-скрипты;
- PySpark-скрипты;
- Airflow DAG;
- отчёт;
- скриншоты выполнения в Yandex Cloud;
- ссылки на DataLens-дашборд или скриншоты дашборда.

Подробная инструкция находится в файле `FULL_GUIDE.md`.
