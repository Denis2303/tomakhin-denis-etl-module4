# Итоговый отчёт

**Студент:** Томахин Денис  
**Дисциплина:** ETL-процессы  
**Модуль:** 4  

## 1. Краткое описание

В рамках итоговой работы был подготовлен учебный ETL-проект в Yandex Cloud.

Фактически были выполнены два блока:

1. перенос данных из YDB в Object Storage через Yandex DataTransfer;
2. обработка CSV-файла через Yandex Data Processing и автоматизация запуска через Apache Airflow.

Kafka и DataLens в облаке не разворачивались. Для Kafka в проекте оставлена подготовленная кодовая часть, но этот блок не считается полностью выполненным.

## 2. Подготовка данных

Для проекта были сгенерированы тестовые данные.

| Файл | Для чего используется | Требуемый объём |
|---|---|---:|
| `transactions_v2.csv` | загрузка в YDB и перенос через DataTransfer | больше 30 МБ |
| `applications.csv` | обработка через PySpark | больше 50 МБ |
| `kafka_loan_events.jsonl` | заготовка для Kafka-блока | больше 20 МБ |

Скрипты генерации находятся в папке:

```text
data_generators
```

Проверка размеров выполнялась скриптом:

```text
scripts/local_size_check.py
```

Скриншот проверки размеров:

```text
screenshots/01_local_data_sizes.png
```

## 3. Задание 1. YDB и DataTransfer

Для первого задания использовался файл:

```text
transactions_v2.csv
```

В YDB была создана таблица:

```text
transactions_v2
```

Скрипт создания таблицы:

```text
yql/create_transactions_v2.yql
```

После создания таблицы CSV-файл был загружен в YDB.

Проверка данных выполнялась через YQL-скрипт:

```text
yql/check_transactions_v2.yql
```

После загрузки таблицы был настроен Yandex DataTransfer:

```text
YDB -> Object Storage
```

Transfer был запущен в режиме копирования данных. После выполнения данные появились в Object Storage в виде JSON-файлов.

Скриншоты по заданию:

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

Для обработки был подготовлен PySpark-скрипт:

```text
spark/process_applications.py
```

Скрипт выполняет базовую ETL-обработку:

1. читает CSV-файл из Object Storage;
2. приводит поля к нужным типам;
3. очищает данные;
4. формирует итоговую таблицу заявок;
5. формирует агрегированные таблицы;
6. сохраняет результат в Object Storage в формате parquet.

Результаты ручного запуска сохранялись в папку:

```text
processed/applications
```

Основные выходные папки:

```text
processed/applications/applications_clean
processed/applications/applications_daily_summary
processed/applications/applications_monthly_summary
```

PySpark job был успешно запущен вручную в Yandex Data Processing. После проверки ручной кластер был удалён.

Скриншоты по ручному запуску:

```text
screenshots/08_dataproc_cluster_running.png
screenshots/09_dataproc_pyspark_job_finished.png
screenshots/10_dataproc_output_files.png
```

## 5. Airflow-автоматизация

Для автоматизации второго задания был создан Managed Airflow.

DAG находится в файле:

```text
dags/dataproc_applications_dag.py
```

DAG состоит из трёх задач:

```text
create_dataproc_cluster
run_applications_pyspark
delete_dataproc_cluster
```

Логика DAG:

1. Airflow создаёт временный Data Processing кластер.
2. На этом кластере запускается PySpark-задание.
3. После выполнения кластер удаляется.

DAG был успешно запущен. После запуска результат появился в Object Storage:

```text
processed/applications_airflow_v2
```

Также была проверена очистка временного Data Processing кластера после завершения DAG.

Скриншоты по Airflow:

```text
screenshots/11_airflow_cluster_running.png
screenshots/12_airflow_variables.png
screenshots/14_airflow_dag_success.png
screenshots/15_airflow_output_files.png
screenshots/16_dataproc_cluster_deleted_after_airflow.png
```

## 6. Kafka

Kafka-блок не был полностью развёрнут и проверен в Yandex Cloud.

В репозитории оставлены подготовленные файлы:

```text
data_generators/generate_kafka_events.py
kafka/send_events_to_kafka.py
spark/kafka_flatten.py
```

Эти файлы показывают планируемую логику Kafka-блока:

1. сгенерировать JSON-события;
2. отправить события в Kafka topic;
3. прочитать сообщения через PySpark;
4. разобрать вложенный JSON;
5. сохранить плоскую таблицу.

Так как Managed Kafka не был развёрнут, скриншоты Kafka cluster, topic и Kafka PySpark job в отчёт не добавлялись.

## 7. DataLens

DataLens-дашборд не был собран в Yandex Cloud.

В проекте оставлено описание возможного дашборда:

```text
datalens/dashboard_description.md
```

Дашборд можно было бы построить на основе агрегированных данных после PySpark-обработки.

## 8. Итог

В работе были полностью выполнены два блока:

1. YDB + DataTransfer.
2. Data Processing + Apache Airflow.

В результате были подготовлены:

- генераторы тестовых данных;
- YQL-скрипты для YDB;
- PySpark-скрипт обработки CSV;
- Airflow DAG;
- скриншоты выполнения;
- итоговый отчёт.

Kafka и DataLens остались как подготовленные, но не развёрнутые части проекта.

GitHub-репозиторий:

```text
https://github.com/Denis2303/tomakhin-denis-etl-module4
```
