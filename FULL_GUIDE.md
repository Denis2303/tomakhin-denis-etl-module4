# Инструкция по проекту

Этот файл коротко описывает, как устроен проект и что было сделано в рамках итоговой работы.

Фактически в облаке были выполнены два блока:

1. YDB + DataTransfer.
2. Data Processing + Airflow.

Kafka и DataLens в Yandex Cloud не разворачивались.

## 1. Подготовка локального окружения

Проект запускался на Windows с Python 3.10.

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Генерация данных

В проекте используются три файла данных:

```text
transactions_v2.csv
applications.csv
kafka_loan_events.jsonl
```

Генерация:

```powershell
python data_generators/generate_transactions_v2.py
python data_generators/generate_applications.py
python data_generators/generate_kafka_events.py
```

Проверка размеров:

```powershell
python scripts/local_size_check.py
```

Ожидаемые размеры:

```text
transactions_v2.csv > 30 MB
applications.csv > 50 MB
kafka_loan_events.jsonl > 20 MB
```

Файл `kafka_loan_events.jsonl` был подготовлен заранее, но Kafka-блок в облаке не запускался.

## 3. Задание 1. YDB и DataTransfer

Для первого задания использовался файл:

```text
data/raw/transactions_v2.csv
```

В YDB была создана таблица:

```text
transactions_v2
```

Скрипт создания таблицы:

```text
yql/create_transactions_v2.yql
```

Скрипт проверки:

```text
yql/check_transactions_v2.yql
```

После загрузки данных был настроен DataTransfer:

```text
YDB -> Object Storage
```

Transfer отработал успешно, и данные появились в Object Storage.

## 4. Задание 2. Data Processing и PySpark

Для второго задания использовался файл:

```text
data/raw/applications.csv
```

Файл был загружен в Object Storage.

PySpark-скрипт:

```text
spark/process_applications.py
```

Скрипт читает CSV-файл, приводит типы данных, очищает данные и сохраняет результат в Object Storage.

Основные выходные папки:

```text
processed/applications/applications_clean
processed/applications/applications_daily_summary
processed/applications/applications_monthly_summary
```

PySpark-задание сначала было проверено вручную в Yandex Data Processing.

## 5. Airflow DAG

Для автоматизации обработки использовался DAG:

```text
dags/dataproc_applications_dag.py
```

DAG выполняет три шага:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

То есть Airflow создаёт временный Data Processing кластер, запускает обработку и затем удаляет кластер.

После успешного запуска DAG результат появился в Object Storage:

```text
processed/applications_airflow_v2
```

## 6. Kafka

Kafka-блок в облаке не был развёрнут.

В репозитории оставлены подготовленные файлы:

```text
data_generators/generate_kafka_events.py
kafka/send_events_to_kafka.py
spark/kafka_flatten.py
```

Они показывают планируемую логику: сгенерировать JSON-события, отправить их в Kafka topic, прочитать topic через PySpark и сохранить плоскую таблицу.

## 7. DataLens

DataLens-дашборд не был собран в Yandex Cloud.

В репозитории оставлено описание возможного дашборда:

```text
datalens/dashboard_description.md
```

Его можно было бы построить на основе агрегированных данных после PySpark-обработки.

## 8. Отчёт и скриншоты

Итоговый отчёт:

```text
report/final_report.md
```

Чек-лист скриншотов:

```text
report/screenshots_checklist.md
```
