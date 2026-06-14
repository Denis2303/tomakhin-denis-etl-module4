import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode_outer, from_json, to_timestamp
from pyspark.sql.types import ArrayType, IntegerType, StringType, StructField, StructType

if len(sys.argv) < 4:
    raise ValueError('Usage: kafka_flatten.py <bootstrap_servers> <topic> <output_path>')

bootstrap_servers = sys.argv[1]
topic = sys.argv[2]
output_path = sys.argv[3]
security_protocol = sys.argv[4] if len(sys.argv) > 4 else ''
sasl_mechanism = sys.argv[5] if len(sys.argv) > 5 else ''
jaas_config = sys.argv[6] if len(sys.argv) > 6 else ''

spark = SparkSession.builder.appName('kafka-loan-events-flatten').getOrCreate()

schema = StructType([
    StructField('application_id', StringType(), True),
    StructField('customer', StructType([
        StructField('customer_id', StringType(), True),
        StructField('region', StringType(), True)
    ]), True),
    StructField('loan', StructType([
        StructField('amount', IntegerType(), True),
        StructField('term_months', IntegerType(), True)
    ]), True),
    StructField('scoring', StructType([
        StructField('score', IntegerType(), True),
        StructField('risk_level', StringType(), True)
    ]), True),
    StructField('documents', ArrayType(StructType([
        StructField('type', StringType(), True),
        StructField('status', StringType(), True)
    ])), True),
    StructField('decision_status', StringType(), True),
    StructField('submitted_at', StringType(), True)
])

reader = spark.read.format('kafka') \
    .option('kafka.bootstrap.servers', bootstrap_servers) \
    .option('subscribe', topic) \
    .option('startingOffsets', 'earliest') \
    .option('endingOffsets', 'latest')

if security_protocol:
    reader = reader.option('kafka.security.protocol', security_protocol)
if sasl_mechanism:
    reader = reader.option('kafka.sasl.mechanism', sasl_mechanism)
if jaas_config:
    reader = reader.option('kafka.sasl.jaas.config', jaas_config)

kafka_df = reader.load()

parsed_df = kafka_df.selectExpr('CAST(value AS STRING) AS json_value') \
    .withColumn('event', from_json(col('json_value'), schema)) \
    .select('event.*')

flat_df = parsed_df.withColumn('document', explode_outer(col('documents'))) \
    .select(
        col('application_id'),
        col('customer.customer_id').alias('customer_id'),
        col('customer.region').alias('region_code'),
        col('loan.amount').alias('loan_amount'),
        col('loan.term_months').alias('term_months'),
        col('scoring.score').alias('score'),
        col('scoring.risk_level').alias('risk_level'),
        col('document.type').alias('document_type'),
        col('document.status').alias('document_status'),
        col('decision_status'),
        to_timestamp(col('submitted_at')).alias('submitted_ts')
    )

summary_df = flat_df.groupBy('region_code', 'risk_level', 'decision_status').count()

flat_df.write.mode('overwrite').parquet(f'{output_path}/kafka_events_flat')
summary_df.write.mode('overwrite').parquet(f'{output_path}/kafka_events_summary')

flat_df.show(20, truncate=False)
summary_df.show(20, truncate=False)

spark.stop()
