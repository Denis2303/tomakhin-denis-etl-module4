# Чек-лист скриншотов

## Выполнено. Задание 1

- [ ] Размер локального файла `transactions_v2.csv` больше 30 МБ.
- [ ] YDB database создана.
- [ ] Таблица `transactions_v2` создана.
- [ ] Проверочный YQL-запрос показывает, что данные загружены.
- [ ] DataTransfer source endpoint настроен на YDB.
- [ ] DataTransfer target endpoint настроен на Object Storage.
- [ ] Transfer завершился успешно.
- [ ] В Object Storage появились файлы выгрузки из YDB.

## Выполнено. Задание 2

- [ ] Файл `applications.csv` больше 50 МБ.
- [ ] Файл `applications.csv` загружен в Object Storage.
- [ ] Файл `process_applications.py` загружен в Object Storage.
- [ ] Data Processing cluster был создан для ручного теста.
- [ ] PySpark job вручную завершился успешно.
- [ ] В Object Storage появились результаты ручной обработки.
- [ ] Managed Airflow создан.
- [ ] Airflow Variables настроены.
- [ ] DAG виден в Airflow UI.
- [ ] DAG завершился успешно.
- [ ] В Object Storage появились результаты Airflow-запуска.
- [ ] Временный Data Processing cluster после DAG удалён.

## Не выполнялось в облаке

### Задание 3. Kafka

- Managed Kafka cluster не разворачивался.
- Kafka topic не создавался.
- Kafka PySpark job не запускался.
- В репозитории оставлена только подготовленная кодовая часть.

### Задание 4. DataLens

- DataLens dashboard не собирался.
- В репозитории оставлено только описание возможного дашборда.
