# Итоговая практическая работа. Модуль 4. ETL-процессы

Студент: Томахин Денис

## Цель работы

Целью работы была реализация дополнительного ETL/Streaming-контура для корпоративной платформы данных с использованием сервисов Yandex Cloud.

В рамках работы были выполнены четыре блока:

1. Перенос данных из YDB в Object Storage через Yandex Data Transfer.
2. Автоматизация обработки файлов с помощью Yandex Data Processing и Apache Airflow.
3. Чтение Kafka-топика с помощью PySpark-задания и разбор вложенного JSON в плоский вид.
4. Построение аналитического дашборда в Yandex DataLens.

## Архитектура решения

Общая логика решения:

```text
CSV/JSON generators
        |
        |-- transactions_v2.csv -> YDB -> Data Transfer -> Object Storage
        |
        |-- applications.csv -> Object Storage -> Data Processing PySpark -> Object Storage
        |
        |-- kafka_loan_events.jsonl -> Kafka topic -> Data Processing PySpark -> Object Storage
        |
        |-- processed datasets -> DataLens dashboard
```

## Подготовка тестовых данных

Для выполнения задания были подготовлены три набора данных.

### transactions_v2

Файл используется для первого задания. Объём файла больше 30 МБ.

Поля:

```text
call_id, call_time, client_id, region_code, campaign_type, call_status, client_response, duration_sec, follow_up_required
```

Скрипт генерации:

```text
data_generators/generate_transactions_v2.py
```

Размер файла: `[ВСТАВИТЬ РАЗМЕР]`

### applications

Файл используется для второго задания. Объём файла больше 50 МБ.

Поля:

```text
application_id, event_time, customer_id, region_code, product_type, requested_amount, term_months, credit_score, risk_level, decision_status, approved_amount, channel, employee_review_flag, processing_time_sec
```

Скрипт генерации:

```text
data_generators/generate_applications.py
```

Размер файла: `[ВСТАВИТЬ РАЗМЕР]`

### kafka_loan_events

Файл используется для третьего задания. Объём файла больше 20 МБ.

Скрипт генерации:

```text
data_generators/generate_kafka_events.py
```

Размер файла: `[ВСТАВИТЬ РАЗМЕР]`

## Задание 1. Yandex Data Transfer

Для выполнения задания была создана база данных YDB.

В базе была создана таблица `transactions_v2`. Скрипт создания таблицы находится в репозитории:

```text
yql/create_transactions_v2.yql
```

После создания таблицы в неё был загружен CSV-файл `transactions_v2.csv`.

Проверочный запрос находится в файле:

```text
yql/check_transactions_v2.yql
```

Количество строк в таблице: `[ВСТАВИТЬ КОЛИЧЕСТВО]`

Скриншот YDB-таблицы:

`[ВСТАВИТЬ СКРИНШОТ]`

Далее был настроен Yandex Data Transfer:

- source endpoint: YDB;
- target endpoint: Object Storage;
- тип трансфера: snapshot;
- путь выгрузки: `datatransfer/transactions_v2/`.

После запуска transfer завершился успешно, а данные появились в Object Storage.

Скриншот Data Transfer:

`[ВСТАВИТЬ СКРИНШОТ]`

Скриншот Object Storage:

`[ВСТАВИТЬ СКРИНШОТ]`

## Задание 2. Yandex Data Processing и Apache Airflow

Для обработки файла `applications.csv` было подготовлено PySpark-задание:

```text
spark/process_applications.py
```

Задание выполняет следующие действия:

1. Читает CSV-файл из Object Storage.
2. Приводит поля к нужным типам.
3. Добавляет технические и аналитические поля.
4. Формирует очищенную таблицу заявок.
5. Формирует дневную агрегацию.
6. Формирует месячную агрегацию.
7. Сохраняет результат в Object Storage в формате parquet.

В результате создаются папки:

```text
applications_clean
applications_daily_summary
applications_monthly_summary
applications_rejected_rows
```

Скриншот PySpark job:

`[ВСТАВИТЬ СКРИНШОТ]`

Скриншот результата в Object Storage:

`[ВСТАВИТЬ СКРИНШОТ]`

Для автоматизации был подготовлен Airflow DAG:

```text
dags/dataproc_applications_dag.py
```

DAG состоит из трёх задач:

1. Создание Data Processing cluster.
2. Запуск PySpark job.
3. Удаление Data Processing cluster.

Скриншот DAG:

`[ВСТАВИТЬ СКРИНШОТ]`

## Задание 3. Kafka и PySpark

Для потоковой части был создан Kafka topic:

```text
loan-applications
```

В topic были отправлены JSON-события из файла:

```text
data/raw/kafka_loan_events.jsonl
```

Скрипт отправки сообщений:

```text
kafka/send_events_to_kafka.py
```

Для чтения Kafka topic было подготовлено PySpark-задание:

```text
spark/kafka_flatten.py
```

Задание выполняет следующие действия:

1. Читает сообщения из Kafka topic.
2. Преобразует поле `value` из строки в JSON.
3. Разбирает вложенные объекты `customer`, `loan`, `scoring`, `documents`.
4. Разворачивает массив `documents`.
5. Сохраняет плоскую таблицу в Object Storage.
6. Строит агрегированную витрину по региону, риску и статусу решения.

Итоговые папки:

```text
kafka_events_flat
kafka_events_summary
```

Скриншот Kafka topic:

`[ВСТАВИТЬ СКРИНШОТ]`

Скриншот PySpark job:

`[ВСТАВИТЬ СКРИНШОТ]`

Скриншот результата в Object Storage:

`[ВСТАВИТЬ СКРИНШОТ]`

## Задание 4. DataLens

В DataLens был создан дашборд для анализа загруженных и обработанных данных.

В дашборд были добавлены следующие визуализации:

1. Количество заявок по дням.
2. Количество заявок по регионам.
3. Распределение заявок по статусу решения.
4. Средний credit score по уровню риска.
5. Сумма requested amount и approved amount по продуктам.
6. Детальная таблица по регионам, продуктам и risk level.

Ссылка на DataLens dashboard:

`[ВСТАВИТЬ ССЫЛКУ]`

Скриншот DataLens dashboard:

`[ВСТАВИТЬ СКРИНШОТ]`

## Итог

В результате работы был реализован учебный ETL/Streaming-проект на базе сервисов Yandex Cloud. Были подготовлены данные, реализованы SQL/YQL-скрипты, PySpark-задания, Airflow DAG и DataLens-дашборд.

Репозиторий GitHub:

`[ВСТАВИТЬ ССЫЛКУ НА PUBLIC GITHUB]`
