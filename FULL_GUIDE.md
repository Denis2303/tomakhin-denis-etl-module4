# Полный гайд для выполнения ДЗ

Этот гайд написан так, чтобы идти по нему с нуля. Лучше выполнять шаги по порядку и после каждого крупного блока делать скриншот.

## 0. Что в итоге должно получиться

Нужно сдать public GitHub-репозиторий. В нём должны лежать код, SQL/YQL-скрипты, PySpark-задания, Airflow DAG и отчёт. В отчёте должны быть описаны действия и приложены скриншоты из Yandex Cloud.

По заданию нужно закрыть 4 блока:

1. Сделать YDB-таблицу `transactions_v2`, загрузить туда CSV от 30 МБ и перенести данные в Object Storage через Data Transfer.
2. Сделать PySpark-обработку CSV от 50 МБ в Yandex Data Processing и автоматизировать запуск через Airflow DAG.
3. Отправить JSON-события от 20 МБ в Kafka, прочитать топик через PySpark, разложить JSON в плоский вид.
4. Построить DataLens-дашборд по итоговым таблицам.

## 1. Что скачать на компьютер

### 1.1. Python

Скачать Python 3.11 с сайта python.org.

Во время установки на Windows обязательно поставить галочку `Add Python to PATH`.

Проверка:

```bash
python --version
```

Должно быть примерно так:

```text
Python 3.11.x
```

### 1.2. Git

Скачать Git с сайта git-scm.com.

Проверка:

```bash
git --version
```

### 1.3. VS Code

Скачать Visual Studio Code.

Он нужен, чтобы удобно открыть папку проекта и редактировать файлы.

### 1.4. Yandex Cloud CLI

Установить `yc` по инструкции Yandex Cloud.

Проверка:

```bash
yc --version
```

Потом выполнить:

```bash
yc init
```

В браузере нужно будет авторизоваться, выбрать cloud и folder.

Проверка текущей папки:

```bash
yc config list
```

### 1.5. AWS CLI

Он нужен для загрузки файлов в Yandex Object Storage.

Проверка:

```bash
aws --version
```

### 1.6. YDB CLI

Он нужен для создания таблицы и загрузки CSV в YDB.

Проверка:

```bash
ydb version
```

## 2. Подготовка проекта локально

Открыть терминал в папке, куда распакован проект.

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать на Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Если PowerShell ругается на политику выполнения:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Потом снова:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить библиотеки:

```bash
pip install -r requirements.txt
```

Сгенерировать данные:

```bash
python data_generators/generate_transactions_v2.py
python data_generators/generate_applications.py
python data_generators/generate_kafka_events.py
python scripts/local_size_check.py
```

Ожидаемый результат:

```text
data/raw/transactions_v2.csv 35 MB
data/raw/applications.csv 60 MB
data/raw/kafka_loan_events.jsonl 25 MB
```

Если размер чуть отличается, это нормально. Главное, чтобы было больше 30, 50 и 20 МБ соответственно.

## 3. Загрузка проекта в GitHub

Создать на GitHub новый репозиторий.

Название можно сделать таким:

```text
tomakhin-denis-etl-module4
```

Репозиторий должен быть `Public`.

В терминале внутри проекта выполнить:

```bash
git init
git add .
git commit -m "initial etl exam project"
git branch -M main
git remote add origin https://github.com/YOUR_LOGIN/tomakhin-denis-etl-module4.git
git push -u origin main
```

Вместо `YOUR_LOGIN` поставить свой логин GitHub.

Файлы данных в GitHub лучше не грузить, потому что они большие. Они добавлены в `.gitignore`. В репозитории должны лежать генераторы данных.

## 4. Создание ресурсов Yandex Cloud

Перед началом нужно понимать: облачные сервисы могут стоить денег. После проверки работы ресурсы надо удалить или остановить.

### 4.1. Создать Object Storage bucket

В консоли Yandex Cloud:

1. Открыть свой folder.
2. Найти `Object Storage`.
3. Нажать `Create bucket`.
4. Имя сделать уникальным, например:

```text
etl-exam-denis-2026
```

5. Доступ оставить приватным.
6. Создать bucket.

Нужно запомнить имя bucket.

### 4.2. Создать service account

В консоли:

1. Открыть `Service accounts`.
2. Нажать `Create service account`.
3. Имя:

```text
etl-exam-sa
```

4. Назначить роли на folder:

```text
storage.editor
ydb.editor
datatransfer.editor
dataproc.editor
managed-kafka.editor
managed-airflow.integrationProvider
iam.serviceAccounts.user
vpc.user
```

Для учебной работы можно выдать шире, но после сдачи лучше удалить service account.

### 4.3. Создать статический ключ для Object Storage

В service account открыть вкладку ключей и создать `Static access key`.

Сохранить:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Настроить AWS CLI:

```bash
aws configure
```

Ввести access key, secret key, регион можно поставить:

```text
ru-central1
```

Проверить bucket:

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 ls
```

## 5. Задание 1. YDB + Data Transfer

### 5.1. Создать YDB database

В консоли Yandex Cloud:

1. Открыть `YDB`.
2. Нажать `Create database`.
3. Тип выбрать serverless, если доступен.
4. Имя:

```text
etl-exam-ydb
```

5. Создать базу.

После создания открыть базу и найти:

```text
Endpoint
Database
```

Они понадобятся для YDB CLI.

### 5.2. Создать таблицу transactions_v2

Вариант через консоль:

1. Открыть YDB database.
2. Открыть вкладку SQL или Query.
3. Вставить содержимое файла:

```text
yql/create_transactions_v2.yql
```

4. Запустить.

Вариант через терминал:

```bash
ydb -e grpcs://YDB_ENDPOINT -d YDB_DATABASE yql -f yql/create_transactions_v2.yql
```

Здесь нужно заменить `YDB_ENDPOINT` и `YDB_DATABASE` на значения из консоли. Если endpoint уже начинается с `grpcs://`, второй раз `grpcs://` писать не надо.

### 5.3. Загрузить CSV в YDB

Команда выглядит так:

```bash
ydb -e grpcs://YDB_ENDPOINT -d YDB_DATABASE import file csv --path transactions_v2 --input-file data/raw/transactions_v2.csv --header --delimiter ","
```

Если endpoint уже полный, использовать так:

```bash
ydb -e FULL_YDB_ENDPOINT -d FULL_YDB_DATABASE import file csv --path transactions_v2 --input-file data/raw/transactions_v2.csv --header --delimiter ","
```

Проверка количества строк:

```bash
ydb -e FULL_YDB_ENDPOINT -d FULL_YDB_DATABASE yql -f yql/check_transactions_v2.yql
```

Нужно сделать скриншот, где видно количество строк.

### 5.4. Создать Data Transfer из YDB в Object Storage

В консоли Yandex Cloud:

1. Открыть `Data Transfer`.
2. Создать source endpoint.
3. Тип источника выбрать `YDB`.
4. Указать созданную YDB database.
5. Создать target endpoint.
6. Тип назначения выбрать `Object Storage`.
7. Указать bucket.
8. Путь можно сделать:

```text
datatransfer/transactions_v2/
```

9. Создать transfer.
10. Тип трансфера выбрать snapshot.
11. Активировать transfer.

После завершения статус должен быть успешным.

Проверить файлы в bucket:

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 ls s3://etl-exam-denis-2026/datatransfer/transactions_v2/ --recursive
```

Нужно сделать скриншоты:

- YDB table с данными;
- Data Transfer со статусом success/done;
- Object Storage с выгруженными файлами.

## 6. Задание 2. Data Processing + Airflow

### 6.1. Загрузить входной CSV и PySpark-файл в Object Storage

Заменить имя bucket на своё:

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 cp data/raw/applications.csv s3://etl-exam-denis-2026/input/applications/applications.csv
aws --endpoint-url=https://storage.yandexcloud.net s3 cp spark/process_applications.py s3://etl-exam-denis-2026/scripts/process_applications.py
```

Проверка:

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 ls s3://etl-exam-denis-2026/ --recursive
```

### 6.2. Создать Data Processing cluster вручную для теста

В консоли:

1. Открыть `Data Processing`.
2. Нажать `Create cluster`.
3. Имя:

```text
etl-exam-dataproc-test
```

4. Выбрать минимальные ресурсы.
5. Включить компоненты:

```text
HDFS
YARN
SPARK
HIVE
```

6. Указать service account `etl-exam-sa`.
7. Указать bucket для логов.
8. Создать кластер.

### 6.3. Запустить PySpark job вручную

В кластере открыть вкладку `Jobs`.

Нажать `Submit job`.

Тип:

```text
PySpark
```

Main python file:

```text
s3a://etl-exam-denis-2026/scripts/process_applications.py
```

Arguments:

```text
s3a://etl-exam-denis-2026/input/applications/applications.csv s3a://etl-exam-denis-2026/output/applications
```

Запустить job.

После успешного выполнения проверить результат:

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 ls s3://etl-exam-denis-2026/output/applications/ --recursive
```

Нужно сделать скриншоты:

- Data Processing cluster;
- PySpark job со статусом Done;
- Object Storage output folders.

После проверки тестовый кластер удалить, чтобы не тратить деньги.

### 6.4. Airflow DAG

Файл DAG уже есть:

```text
dags/dataproc_applications_dag.py
```

Он делает 3 действия:

1. Создаёт Data Processing cluster.
2. Запускает PySpark job `process_applications.py`.
3. Удаляет cluster даже при ошибке job.

Нужно загрузить DAG в Managed Airflow.

В Managed Airflow нужно создать переменные:

```text
YC_FOLDER_ID
YC_SUBNET_ID
YC_SERVICE_ACCOUNT_ID
YC_BUCKET_NAME
YC_ZONE
YC_DATAPROC_CLUSTER_NAME
APPLICATIONS_INPUT_PATH
APPLICATIONS_OUTPUT_PATH
APPLICATIONS_PYSPARK_FILE
```

Значения:

```text
YC_ZONE=ru-central1-a
YC_DATAPROC_CLUSTER_NAME=etl-exam-dataproc-airflow
APPLICATIONS_INPUT_PATH=s3a://etl-exam-denis-2026/input/applications/applications.csv
APPLICATIONS_OUTPUT_PATH=s3a://etl-exam-denis-2026/output/airflow_applications
APPLICATIONS_PYSPARK_FILE=s3a://etl-exam-denis-2026/scripts/process_applications.py
```

Ещё нужна Airflow connection:

```text
yandexcloud_default
```

В ней должен быть настроен доступ к Yandex Cloud.

После запуска DAG нужно сделать скриншоты:

- DAG в Airflow;
- успешные task: create, run, delete;
- результат в Object Storage.

## 7. Задание 3. Kafka + PySpark

### 7.1. Создать Managed Kafka cluster

В консоли Yandex Cloud:

1. Открыть `Managed Service for Apache Kafka`.
2. Создать cluster.
3. Имя:

```text
etl-exam-kafka
```

4. Использовать минимальные ресурсы.
5. Создать пользователя, например:

```text
etl_user
```

6. Задать пароль.
7. Создать topic:

```text
loan-applications
```

### 7.2. Отправить события в Kafka

Сначала нужно задать переменные окружения.

Windows PowerShell:

```powershell
$env:KAFKA_BOOTSTRAP_SERVERS="broker1:9091,broker2:9091"
$env:KAFKA_TOPIC="loan-applications"
$env:KAFKA_USERNAME="etl_user"
$env:KAFKA_PASSWORD="YOUR_PASSWORD"
$env:KAFKA_SECURITY_PROTOCOL="SASL_SSL"
$env:KAFKA_SASL_MECHANISM="SCRAM-SHA-512"
```

macOS/Linux:

```bash
export KAFKA_BOOTSTRAP_SERVERS="broker1:9091,broker2:9091"
export KAFKA_TOPIC="loan-applications"
export KAFKA_USERNAME="etl_user"
export KAFKA_PASSWORD="YOUR_PASSWORD"
export KAFKA_SECURITY_PROTOCOL="SASL_SSL"
export KAFKA_SASL_MECHANISM="SCRAM-SHA-512"
```

Запуск отправки:

```bash
python kafka/send_events_to_kafka.py data/raw/kafka_loan_events.jsonl
```

Нужно дождаться, пока будут отправлены сообщения.

### 7.3. Загрузить Kafka PySpark-файл в Object Storage

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 cp spark/kafka_flatten.py s3://etl-exam-denis-2026/scripts/kafka_flatten.py
```

### 7.4. Запустить PySpark job для чтения Kafka

В Data Processing cluster открыть `Jobs` и создать PySpark job.

Main python file:

```text
s3a://etl-exam-denis-2026/scripts/kafka_flatten.py
```

Packages:

```text
org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2
```

Arguments без авторизации:

```text
broker1:9092,broker2:9092 loan-applications s3a://etl-exam-denis-2026/output/kafka
```

Arguments с SASL_SSL:

```text
broker1:9091,broker2:9091 loan-applications s3a://etl-exam-denis-2026/output/kafka SASL_SSL SCRAM-SHA-512 org.apache.kafka.common.security.scram.ScramLoginModule required username="etl_user" password="YOUR_PASSWORD";
```

После выполнения проверить результат:

```bash
aws --endpoint-url=https://storage.yandexcloud.net s3 ls s3://etl-exam-denis-2026/output/kafka/ --recursive
```

Нужно сделать скриншоты:

- Kafka cluster;
- topic `loan-applications`;
- отправка сообщений;
- PySpark job Done;
- parquet output в Object Storage.

## 8. Задание 4. DataLens

Самый простой вариант для сдачи:

1. Взять итоговые parquet/CSV из Object Storage.
2. Подключить их как источник данных в DataLens через Yandex Cloud connection.
3. Создать dataset.
4. Создать charts.
5. Собрать dashboard.

Рекомендуемые графики:

1. Количество заявок по дням.
2. Количество заявок по регионам.
3. Доля approved/rejected/manual_review.
4. Средний credit_score по risk_level.
5. Сумма requested_amount и approved_amount по продуктам.
6. Таблица с детализацией по region_code, product_type, risk_level.

Подробное описание есть в файле:

```text
datalens/dashboard_description.md
```

Нужно сделать скриншоты:

- dataset;
- charts;
- dashboard.

Если получится сделать публичную ссылку на dashboard, её надо добавить в отчёт.

## 9. Заполнение отчёта

Шаблон лежит здесь:

```text
report/final_report_template.md
```

Нужно заменить места вида:

```text
[ВСТАВИТЬ СКРИНШОТ]
[ВСТАВИТЬ ССЫЛКУ]
[ВСТАВИТЬ КОЛИЧЕСТВО]
```

После заполнения можно переименовать файл:

```text
report/final_report.md
```

## 10. Что удалить после проверки

После того как всё проверено и скриншоты сделаны, удалить или остановить:

1. Data Processing clusters.
2. Managed Kafka cluster.
3. Managed Airflow cluster.
4. Data Transfer endpoints и transfers.
5. YDB database, если больше не нужна.
6. Object Storage bucket, если больше не нужен.
7. Service account keys.

Это важно, чтобы не списывались деньги.

## 11. Минимальный чек-лист перед сдачей

Перед отправкой в LMS проверить:

- GitHub repository public.
- В названии репозитория есть фамилия, имя и тема задания.
- В репозитории есть `README.md`.
- Есть YQL-скрипты.
- Есть PySpark-скрипты.
- Есть Airflow DAG.
- Есть отчёт.
- В отчёте есть скриншоты YDB, Data Transfer, Object Storage, Data Processing, Airflow, Kafka, DataLens.
- В LMS вставлена ссылка на GitHub.
