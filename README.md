# Томахин Денис. Итоговое ДЗ. Модуль 4. ETL-процессы

Проект подготовлен для итоговой практической работы по дисциплине «ETL-процессы».

В работе реализованы два основных блока:

1. перенос данных из YDB в Object Storage через Yandex DataTransfer;
2. обработка CSV-файла через Yandex Data Processing и автоматизация запуска через Apache Airflow.

Kafka и DataLens в облаке не разворачивались. Для Kafka в репозитории оставлена подготовленная кодовая часть, но в итоговом отчёте этот блок не считается выполненным.

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
│   ├── final_report.md
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

Проект запускался на Windows с Python 3.10.

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

## Что было выполнено

### Задание 1. YDB и DataTransfer

Файл `transactions_v2.csv` был загружен в таблицу `transactions_v2` в YDB.

Для создания и проверки таблицы используются YQL-скрипты:

```text
yql/create_transactions_v2.yql
yql/check_transactions_v2.yql
```

После загрузки таблицы был настроен перенос данных:

```text
YDB -> Object Storage
```

DataTransfer успешно выгрузил данные из YDB в Object Storage.

### Задание 2. Data Processing и Airflow

Файл `applications.csv` был загружен в Object Storage и обработан PySpark-скриптом:

```text
spark/process_applications.py
```

Сначала PySpark-задание было проверено вручную в Yandex Data Processing.

После этого был настроен Airflow DAG:

```text
dags/dataproc_applications_dag.py
```

DAG создаёт временный Data Processing кластер, запускает PySpark-задание и удаляет кластер после выполнения.

## Что не разворачивалось

Kafka-блок не был полностью развёрнут и проверен в Yandex Cloud.

DataLens-дашборд также не был собран в облаке.

При этом в репозитории оставлены заготовки для Kafka и DataLens, чтобы было понятно, как планировалось продолжить проект.

## Отчёт

Итоговый отчёт находится здесь:

```text
report/final_report.md
```
