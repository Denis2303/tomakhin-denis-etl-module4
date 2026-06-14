# Итоговый отчёт

**Студент:** Томахин Денис  
**Дисциплина:** ETL-процессы  
**Модуль:** 4  

## 1. Краткое описание проекта

В рамках работы был подготовлен проект по построению ETL-процессов в Yandex Cloud.

В проекте реализованы:

- генерация тестовых данных нужного объёма;
- загрузка данных в YDB;
- перенос данных из YDB в Object Storage через DataTransfer;
- обработка CSV-файла через PySpark в Yandex Data Processing;
- автоматизация PySpark-обработки через Apache Airflow;
- подготовка Kafka-блока на уровне кода;
- подготовка описания DataLens-дашборда.

## 2. Локальная генерация данных

Для работы были подготовлены три набора данных:

| Файл | Назначение | Размер |
|---|---|---:|
| `transactions_v2.csv` | данные для YDB и DataTransfer | больше 30 МБ |
| `applications.csv` | данные для PySpark-обработки | больше 50 МБ |
| `kafka_loan_events.jsonl` | JSON-события для Kafka | больше 20 МБ |

Данные генерировались локально с помощью Python-скриптов из папки `data_generators`.

Проверка размеров выполнялась скриптом:

```text
scripts/local_size_check.py
```

Скриншот:

```text
screenshots/01_local_data_sizes.png
```

## 3. Задание 1. YDB и DataTransfer

Для первого задания была создана YDB-база данных и таблица:

```text
transactions_v2
```

Таблица создавалась с помощью YQL-скрипта:

```text
yql/create_transactions_v2.yql
```

После этого в таблицу был загружен CSV-файл `transactions_v2.csv`.

Проверка количества строк выполнялась скриптом:

```text
yql/check_transactions_v2.yql
```

После загрузки данных был настроен DataTransfer:

```text
YDB -> Object Storage
```

Transfer был запущен в режиме копирования данных. После завершения в Object Storage появились выгруженные JSON-файлы с данными из таблицы `transactions_v2`.

Скриншоты:

```text
screenshots/04_ydb_transactions_loaded.png
screenshots/05_datatransfer_created.png
screenshots/06_datatransfer_completed.png
screenshots/07_datatransfer_object_storage_result.png
```

## 4. Задание 2. Data Processing и PySpark

Для второго задания использовался файл:

```text
applications.csv
```

Файл был загружен в Object Storage.

Для обработки использовался PySpark-скрипт:

```text
spark/process_applications.py
```

Скрипт читает CSV-файл, приводит типы данных, очищает данные и сохраняет результат в Object Storage.

В результате обработки формируются папки:

```text
processed/applications/applications_clean
processed/applications/applications_daily_summary
processed/applications/applications_monthly_summary
```

Сначала PySpark-задание было запущено вручную в Yandex Data Processing. После успешной проверки ручной кластер был удалён.

Скриншоты:

```text
screenshots/08_dataproc_cluster_running.png
screenshots/09_dataproc_pyspark_job_finished.png
screenshots/10_dataproc_output_files.png
```

## 5. Airflow-автоматизация

Для автоматизации обработки был создан Managed Airflow.

DAG находится в файле:

```text
dags/dataproc_applications_dag.py
```

DAG выполняет три задачи:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

Логика такая: Airflow создаёт временный Data Processing кластер, запускает PySpark-задание, а после выполнения удаляет кластер. Это позволяет не держать Data Processing постоянно включённым.

DAG был успешно запущен. После выполнения появились результаты в Object Storage:

```text
processed/applications_airflow_v2
```

Также была проверена очистка временного Data Processing кластера после завершения DAG.

Скриншоты:

```text
screenshots/11_airflow_cluster_running.png
screenshots/12_airflow_variables.png
screenshots/14_airflow_dag_success.png
screenshots/15_airflow_output_files.png
screenshots/16_dataproc_cluster_deleted_after_airflow.png
```

## 6. Kafka-блок

Для Kafka-блока в проекте подготовлена кодовая часть:

```text
data_generators/generate_kafka_events.py
kafka/send_events_to_kafka.py
spark/kafka_flatten.py
```

Генератор создаёт JSON-события по заявкам. Скрипт `send_events_to_kafka.py` предназначен для отправки сообщений в Kafka topic. PySpark-скрипт `kafka_flatten.py` читает сообщения из Kafka, разбирает вложенный JSON и сохраняет данные в плоском виде.

Полностью развернуть и проверить Managed Kafka в Yandex Cloud я не успел, поэтому этот блок оставлен как подготовленная кодовая часть без облачного запуска.

## 7. DataLens

Для DataLens подготовлено описание дашборда:

```text
datalens/dashboard_description.md
```

В качестве основы для визуализации можно использовать агрегированные данные после PySpark-обработки.

Планируемые графики:

- количество заявок по дням;
- количество заявок по статусам;
- средняя сумма заявки по уровню риска;
- распределение заявок по регионам.

Если DataLens-дашборд будет собран отдельно, скриншоты можно добавить в папку `screenshots`.

## 8. Итог

В работе были полностью выполнены блоки с YDB/DataTransfer и Data Processing/Airflow.

Kafka-блок подготовлен на уровне кода, но не был развёрнут в облаке. DataLens-блок описан в проекте и может быть собран по результатам PySpark-обработки.

Основные результаты проекта находятся в репозитории:

- YQL-скрипты для YDB;
- PySpark-скрипты;
- Airflow DAG;
- генераторы тестовых данных;
- описание архитектуры;
- отчёт и скриншоты выполнения.
