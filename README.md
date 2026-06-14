# Томахин Денис. Итоговое ДЗ. Модуль 4. ETL-процессы

Проект подготовлен для итоговой практической работы по дисциплине «ETL-процессы».

Цель проекта — реализовать ETL/Streaming-процесс в Yandex Cloud: загрузку данных, перенос между сервисами, обработку через PySpark, автоматизацию через Airflow и подготовку данных для визуализации.

## Реализованные части

1. **Yandex DataTransfer**

   Реализован перенос таблицы `transactions_v2` из Managed Service for YDB в Object Storage.

2. **Yandex Data Processing + Apache Airflow**

   Реализована обработка файла `applications.csv` через PySpark-задание в Yandex Data Processing.

   Airflow DAG автоматизирует процесс:
   - создание Data Processing кластера;
   - запуск PySpark-задания;
   - удаление кластера после выполнения.

3. **Apache Kafka + PySpark**

   Подготовлены скрипты для отправки JSON-событий в Kafka и обработки вложенного JSON через PySpark.

4. **Yandex DataLens**

   Подготовлено описание дашборда для визуализации результатов обработки данных.

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

## Локальный запуск на Windows

Создать виртуальное окружение:

```powershell
py -3.10 -m venv .venv
```

Активировать окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

Сгенерировать данные:

```powershell
python data_generators/generate_transactions_v2.py
python data_generators/generate_applications.py
python data_generators/generate_kafka_events.py
```

Проверить размеры файлов:

```powershell
python scripts/local_size_check.py
```

После генерации появляются файлы:

```text
data/raw/transactions_v2.csv
data/raw/applications.csv
data/raw/kafka_loan_events.jsonl
```

## Основные данные

| Файл | Назначение | Размер |
|---|---|---:|
| `transactions_v2.csv` | данные для загрузки в YDB и переноса через DataTransfer | больше 30 МБ |
| `applications.csv` | входной CSV-файл для обработки через PySpark | больше 50 МБ |
| `kafka_loan_events.jsonl` | JSON-события для Kafka | больше 20 МБ |

## PySpark-обработка applications.csv

Скрипт:

```text
spark/process_applications.py
```

Скрипт читает CSV-файл с заявками, приводит типы данных, формирует очищенную таблицу и агрегированные витрины.

Результаты сохраняются в Object Storage:

```text
processed/applications/applications_clean
processed/applications/applications_daily_summary
processed/applications/applications_monthly_summary
```

## Airflow DAG

Файл DAG:

```text
dags/dataproc_applications_dag.py
```

DAG выполняет три задачи:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

Такой подход позволяет не держать Data Processing кластер постоянно включённым, а создавать его только на время обработки данных.

## YQL-скрипты

В папке `yql` находятся скрипты для работы с таблицей `transactions_v2` в YDB:

```text
create_transactions_v2.yql
check_transactions_v2.yql
sample_transactions_v2.yql
```

## Отчёт

Подробное описание выполненных шагов и скриншоты находятся в папке:

```text
report
```

Дополнительная инструкция по воспроизведению проекта находится в файле:

```text
FULL_GUIDE.md
```
