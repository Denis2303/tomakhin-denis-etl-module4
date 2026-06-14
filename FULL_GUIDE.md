# Инструкция по проекту

Этот файл описывает, как устроен проект и какие шаги были выполнены для итогового задания по ETL-процессам.

Проект делался под Windows, Python 3.10 и сервисы Yandex Cloud.

## 1. Локальная подготовка

Сначала создаётся виртуальное окружение:

```powershell
py -3.10 -m venv .venv
```

Потом оно активируется:

```powershell
.\.venv\Scripts\Activate.ps1
```

После этого устанавливаются зависимости:

```powershell
pip install -r requirements.txt
```

## 2. Генерация данных

В проекте используются три набора данных:

* `transactions_v2.csv` — данные для YDB и DataTransfer;
* `applications.csv` — данные для PySpark-обработки;
* `kafka_loan_events.jsonl` — JSON-события для Kafka.

Файлы генерируются командами:

```powershell
python data_generators/generate_transactions_v2.py
python data_generators/generate_applications.py
python data_generators/generate_kafka_events.py
```

Проверить размеры можно так:

```powershell
python scripts/local_size_check.py
```

Ожидаемый результат:

```text
transactions_v2.csv > 30 MB
applications.csv > 50 MB
kafka_loan_events.jsonl > 20 MB
```

## 3. YDB и DataTransfer

Для первой части задания используется файл `transactions_v2.csv`.

Сначала в YDB создаётся таблица `transactions_v2`. Для этого используется скрипт:

```text
yql/create_transactions_v2.yql
```

После загрузки данных таблица проверяется скриптом:

```text
yql/check_transactions_v2.yql
```

Затем через Yandex DataTransfer был настроен перенос данных:

```text
YDB -> Object Storage
```

Результат выгрузки сохраняется в Object Storage в JSON-формате.

## 4. Data Processing и PySpark

Для второй части задания используется файл `applications.csv`.

Он загружается в Object Storage, после чего обрабатывается PySpark-скриптом:

```text
spark/process_applications.py
```

Скрипт читает CSV-файл, приводит типы данных, очищает данные и формирует итоговые таблицы.

Результаты сохраняются в Object Storage:

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

DAG делает три шага:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

То есть кластер Data Processing не работает постоянно. Он создаётся только на время обработки, запускает PySpark-задание и затем удаляется.

## 6. Kafka

Для Kafka-блока в проекте подготовлены файлы:

```text
data_generators/generate_kafka_events.py
kafka/send_events_to_kafka.py
spark/kafka_flatten.py
```

`generate_kafka_events.py` создаёт JSON-события.

`send_events_to_kafka.py` нужен для отправки сообщений в Kafka topic.

`spark/kafka_flatten.py` читает сообщения из Kafka, разбирает вложенный JSON и сохраняет результат в плоском виде.

Полностью развернуть и проверить Managed Kafka в Yandex Cloud я не успел. Поэтому в репозитории оставлена подготовленная кодовая часть и логика запуска этого блока.

## 7. DataLens

Для DataLens подготовлено описание дашборда:

```text
datalens/dashboard_description.md
```

В качестве источника для визуализации можно использовать агрегированные данные после PySpark-обработки.

Основные варианты графиков:

* количество заявок по дням;
* количество заявок по статусам;
* средняя сумма заявки по уровню риска;
* распределение заявок по регионам.

## 8. Отчёт

Шаблон отчёта находится здесь:

```text
report/final_report_template.md
```

В отчёте описываются выполненные шаги и добавляются скриншоты из Yandex Cloud.

Основные скриншоты:

* размер локальных файлов;
* загруженные файлы в Object Storage;
* таблица в YDB;
* успешный DataTransfer;
* Data Processing job;
* Airflow DAG;
* результаты обработки в Object Storage;
* DataLens dashboard, если он был сделан.
