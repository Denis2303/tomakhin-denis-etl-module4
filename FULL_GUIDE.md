# Инструкция по запуску проекта

В этом файле описаны основные шаги для воспроизведения проекта.

## 1. Подготовка локального окружения

Проект запускался на Windows с Python 3.10.

Создание виртуального окружения:

```powershell
py -3.10 -m venv .venv
```

Активация окружения:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установка зависимостей:

```powershell
pip install -r requirements.txt
```

## 2. Генерация тестовых данных

Для задания используются три набора данных:

```powershell
python data_generators/generate_transactions_v2.py
python data_generators/generate_applications.py
python data_generators/generate_kafka_events.py
```

Проверка размеров файлов:

```powershell
python scripts/local_size_check.py
```

Ожидаемые размеры:

```text
transactions_v2.csv > 30 MB
applications.csv > 50 MB
kafka_loan_events.jsonl > 20 MB
```

## 3. YDB и DataTransfer

Файл `transactions_v2.csv` загружается в таблицу `transactions_v2` в YDB.

Для создания таблицы используется скрипт:

```text
yql/create_transactions_v2.yql
```

Для проверки загрузки используется скрипт:

```text
yql/check_transactions_v2.yql
```

После загрузки таблицы был настроен DataTransfer:

```text
YDB -> Object Storage
```

Результат выгрузки сохраняется в Object Storage в JSON-формате.

## 4. Data Processing и PySpark

Файл `applications.csv` загружается в Object Storage.

PySpark-скрипт:

```text
spark/process_applications.py
```

Скрипт выполняет обработку заявок и сохраняет результат в Object Storage:

```text
processed/applications/applications_clean
processed/applications/applications_daily_summary
processed/applications/applications_monthly_summary
```

## 5. Airflow DAG

Для автоматизации PySpark-обработки используется DAG:

```text
dags/dataproc_applications_dag.py
```

DAG выполняет три задачи:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

Кластер Data Processing создаётся только на время обработки и удаляется после завершения задачи.

## 6. Kafka

Для Kafka подготовлены файлы:

```text
data_generators/generate_kafka_events.py
kafka/send_events_to_kafka.py
spark/kafka_flatten.py
```

`generate_kafka_events.py` создаёт JSON-события.

`send_events_to_kafka.py` отправляет события в Kafka topic.

`kafka_flatten.py` читает сообщения из Kafka, разбирает вложенный JSON и сохраняет плоскую таблицу.

## 7. DataLens

Описание дашборда находится в файле:

```text
datalens/dashboard_description.md
```

Для визуализации используются агрегированные данные после PySpark-обработки.

## 8. Отчёт

Шаблон отчёта находится здесь:

```text
report/final_report_template.md
```

В отчёте описаны выполненные шаги и приложены скриншоты из Yandex Cloud.

## Статус выполнения Kafka-блока

Для Kafka-блока подготовлены генератор JSON-событий, скрипт отправки сообщений в Kafka и PySpark-скрипт для чтения топика и преобразования вложенного JSON в плоскую структуру.

Из-за ограничения по времени Managed Kafka cluster не был полностью развёрнут и проверен в Yandex Cloud. Кодовая часть для этого блока находится в репозитории и может быть использована для последующего запуска.

## Статус по Kafka

Kafka-блок в проекте подготовлен на уровне кода: есть генератор JSON-событий, скрипт для отправки сообщений в Kafka и PySpark-скрипт, который читает данные из топика, разбирает вложенный JSON и сохраняет результат в плоском виде.

Полностью развернуть и проверить Managed Kafka в Yandex Cloud я не успел. Поэтому в репозитории оставил готовую кодовую часть и описание того, как этот блок должен запускаться.
