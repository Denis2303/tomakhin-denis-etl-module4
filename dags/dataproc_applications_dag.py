from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.providers.yandex.operators.dataproc import DataprocCreateClusterOperator, DataprocCreatePysparkJobOperator, DataprocDeleteClusterOperator
from airflow.utils.trigger_rule import TriggerRule

folder_id = Variable.get('YC_FOLDER_ID')
subnet_id = Variable.get('YC_SUBNET_ID')
service_account_id = Variable.get('YC_SERVICE_ACCOUNT_ID')
bucket = Variable.get('YC_BUCKET_NAME')
zone = Variable.get('YC_ZONE', default_var='ru-central1-a')
cluster_name = Variable.get('YC_DATAPROC_CLUSTER_NAME', default_var='etl-exam-dataproc')
input_path = Variable.get('APPLICATIONS_INPUT_PATH')
output_path = Variable.get('APPLICATIONS_OUTPUT_PATH')
main_file = Variable.get('APPLICATIONS_PYSPARK_FILE')

with DAG(
    dag_id='etl_exam_applications_dataproc',
    start_date=datetime(2026, 5, 1),
    schedule_interval=None,
    catchup=False,
    default_args={
        'owner': 'student',
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    }
) as dag:
    create_cluster = DataprocCreateClusterOperator(
        task_id='create_dataproc_cluster',
        folder_id=folder_id,
        cluster_name=cluster_name,
        cluster_description='ETL exam processing cluster',
        cluster_image_version='2.1',
        ssh_public_keys=[],
        subnet_id=subnet_id,
        services=('HDFS', 'YARN', 'SPARK', 'HIVE'),
        s3_bucket=bucket,
        zone=zone,
        service_account_id=service_account_id,
        masternode_resource_preset='s2.small',
        masternode_disk_size=20,
        masternode_disk_type='network-hdd',
        datanode_resource_preset='s2.small',
        datanode_disk_size=20,
        datanode_disk_type='network-hdd',
        datanode_count=1,
        computenode_resource_preset='s2.small',
        computenode_disk_size=20,
        computenode_disk_type='network-hdd',
        computenode_count=1,
        connection_id='yandexcloud_default'
    )

    run_pyspark = DataprocCreatePysparkJobOperator(
        task_id='run_applications_pyspark',
        cluster_id="{{ task_instance.xcom_pull(task_ids='create_dataproc_cluster') }}",
        main_python_file_uri=main_file,
        args=[input_path, output_path],
        name='applications_processing_job',
        connection_id='yandexcloud_default'
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id='delete_dataproc_cluster',
        cluster_id="{{ task_instance.xcom_pull(task_ids='create_dataproc_cluster') }}",
        connection_id='yandexcloud_default',
        trigger_rule=TriggerRule.ALL_DONE
    )

    create_cluster >> run_pyspark >> delete_cluster
