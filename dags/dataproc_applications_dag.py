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
cluster_name = Variable.get('YC_DATAPROC_CLUSTER_NAME', default_var='etl-airflow-dataproc')
input_path = Variable.get('APPLICATIONS_INPUT_PATH')
output_path = Variable.get('APPLICATIONS_OUTPUT_PATH')
main_file = Variable.get('APPLICATIONS_PYSPARK_FILE')
security_group_id = Variable.get('YC_SECURITY_GROUP_ID')

with DAG(
    dag_id='etl_exam_applications_dataproc',
    start_date=datetime(2026, 5, 1),
    schedule_interval=None,
    catchup=False,
    default_args={
        'owner': 'student',
        'retries': 0,
        'retry_delay': timedelta(minutes=5)
    }
) as dag:
    create_cluster = DataprocCreateClusterOperator(
        task_id='create_dataproc_cluster',
        folder_id=folder_id,
        cluster_name=cluster_name,
        cluster_description='ETL exam processing cluster',
        cluster_image_version='2.0',
        ssh_public_keys=[],
        subnet_id=subnet_id,
        services=('YARN', 'SPARK'),
        s3_bucket=bucket,
        zone=zone,
        service_account_id=service_account_id,
        masternode_resource_preset='s2.micro',
        masternode_disk_size=20,
        masternode_disk_type='network-ssd',
        datanode_count=0,
        computenode_resource_preset='s2.micro',
        computenode_disk_size=20,
        computenode_disk_type='network-ssd',
        computenode_count=1,
        connection_id='yandexcloud_default',
        security_group_ids=[security_group_id],
        oslogin_enabled=True
    )

    run_pyspark = DataprocCreatePysparkJobOperator(
        task_id='run_applications_pyspark',
        cluster_id="{{ task_instance.xcom_pull(task_ids='create_dataproc_cluster') }}",
        main_python_file_uri=main_file,
        args=[input_path, output_path],
        name='applications_processing_airflow_job',
        connection_id='yandexcloud_default'
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id='delete_dataproc_cluster',
        cluster_id="{{ task_instance.xcom_pull(task_ids='create_dataproc_cluster') }}",
        connection_id='yandexcloud_default',
        trigger_rule=TriggerRule.ALL_DONE
    )

    create_cluster >> run_pyspark >> delete_cluster
