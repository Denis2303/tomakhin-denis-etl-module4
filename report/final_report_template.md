# Шаблон итогового отчёта

**Студент:** Томахин Денис  
**Дисциплина:** ETL-процессы  
**Модуль:** 4  

## 1. Краткое описание

В работе выполнены два блока:

1. YDB + DataTransfer.
2. Data Processing + Apache Airflow.

Kafka и DataLens в облаке не разворачивались.

## 2. Подготовка данных

Сгенерированные файлы:

```text
transactions_v2.csv
applications.csv
kafka_loan_events.jsonl
```

Скриншот проверки размеров:

```text
screenshots/01_local_data_sizes.png
```

## 3. Задание 1. YDB и DataTransfer

Таблица в YDB:

```text
transactions_v2
```

YQL-скрипты:

```text
yql/create_transactions_v2.yql
yql/check_transactions_v2.yql
```

Transfer:

```text
YDB -> Object Storage
```

Скриншоты:

```text
screenshots/04_ydb_transactions_loaded.png
screenshots/05_datatransfer_created.png
screenshots/06_datatransfer_completed.png
screenshots/07_datatransfer_object_storage_result.png
```

## 4. Задание 2. Data Processing и Airflow

PySpark-скрипт:

```text
spark/process_applications.py
```

Airflow DAG:

```text
dags/dataproc_applications_dag.py
```

Задачи DAG:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

Результат Airflow-запуска:

```text
processed/applications_airflow_v2
```

Скриншоты:

```text
screenshots/08_dataproc_cluster_running.png
screenshots/09_dataproc_pyspark_job_finished.png
screenshots/10_dataproc_output_files.png
screenshots/11_airflow_cluster_running.png
screenshots/12_airflow_variables.png
screenshots/14_airflow_dag_success.png
screenshots/15_airflow_output_files.png
screenshots/16_dataproc_cluster_deleted_after_airflow.png
```

## 5. Невыполненные части

Kafka не был развёрнут в Yandex Cloud. Кодовая часть подготовлена, но облачный запуск не выполнялся.

DataLens dashboard не был собран в Yandex Cloud.

## 6. Итог

Полностью выполнены задания 1 и 2.

GitHub-репозиторий:

```text
https://github.com/Denis2303/tomakhin-denis-etl-module4
```
