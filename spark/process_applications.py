import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, date_format, round, sum, to_date, to_timestamp, when
from pyspark.sql.types import BooleanType, IntegerType, StringType, StructField, StructType

if len(sys.argv) < 3:
    raise ValueError('Usage: process_applications.py <input_path> <output_path>')

input_path = sys.argv[1]
output_path = sys.argv[2]

spark = SparkSession.builder.appName('applications-processing').enableHiveSupport().getOrCreate()

schema = StructType([
    StructField('application_id', StringType(), False),
    StructField('event_time', StringType(), True),
    StructField('customer_id', StringType(), True),
    StructField('region_code', StringType(), True),
    StructField('product_type', StringType(), True),
    StructField('requested_amount', IntegerType(), True),
    StructField('term_months', IntegerType(), True),
    StructField('credit_score', IntegerType(), True),
    StructField('risk_level', StringType(), True),
    StructField('decision_status', StringType(), True),
    StructField('approved_amount', IntegerType(), True),
    StructField('channel', StringType(), True),
    StructField('employee_review_flag', BooleanType(), True),
    StructField('processing_time_sec', IntegerType(), True)
])

raw_df = spark.read.option('header', True).schema(schema).csv(input_path)

prepared_df = raw_df.withColumn('event_ts', to_timestamp(col('event_time'), 'yyyy-MM-dd HH:mm:ss')) \
    .withColumn('event_date', to_date(col('event_ts'))) \
    .withColumn('event_month', date_format(col('event_ts'), 'yyyy-MM')) \
    .withColumn('is_approved', when(col('decision_status') == 'approved', 1).otherwise(0)) \
    .withColumn('is_rejected', when(col('decision_status') == 'rejected', 1).otherwise(0)) \
    .withColumn('is_manual_review', when(col('decision_status') == 'manual_review', 1).otherwise(0)) \
    .withColumn('approval_rate_amount', when(col('requested_amount') > 0, col('approved_amount') / col('requested_amount')).otherwise(0.0))

valid_df = prepared_df.filter(col('application_id').isNotNull() & col('event_ts').isNotNull() & col('region_code').isNotNull())
invalid_df = prepared_df.subtract(valid_df)

summary_df = valid_df.groupBy('event_date', 'region_code', 'product_type', 'risk_level', 'decision_status').agg(
    count('*').alias('applications_count'),
    sum('requested_amount').alias('requested_amount_sum'),
    sum('approved_amount').alias('approved_amount_sum'),
    round(avg('credit_score'), 2).alias('avg_credit_score'),
    round(avg('processing_time_sec'), 2).alias('avg_processing_time_sec'),
    round(avg('approval_rate_amount'), 4).alias('avg_approval_rate_amount')
)

monthly_df = valid_df.groupBy('event_month', 'region_code', 'product_type').agg(
    count('*').alias('applications_count'),
    sum('is_approved').alias('approved_count'),
    sum('is_rejected').alias('rejected_count'),
    sum('is_manual_review').alias('manual_review_count'),
    sum('requested_amount').alias('requested_amount_sum'),
    sum('approved_amount').alias('approved_amount_sum'),
    round(avg('credit_score'), 2).alias('avg_credit_score')
)

valid_df.write.mode('overwrite').parquet(f'{output_path}/applications_clean')
summary_df.write.mode('overwrite').parquet(f'{output_path}/applications_daily_summary')
monthly_df.write.mode('overwrite').parquet(f'{output_path}/applications_monthly_summary')
invalid_df.write.mode('overwrite').parquet(f'{output_path}/applications_rejected_rows')

valid_df.createOrReplaceTempView('applications_clean')
summary_df.createOrReplaceTempView('applications_daily_summary')
monthly_df.createOrReplaceTempView('applications_monthly_summary')

spark.sql('SELECT COUNT(*) AS rows_count FROM applications_clean').show(truncate=False)
spark.sql('SELECT * FROM applications_daily_summary ORDER BY event_date, region_code LIMIT 20').show(truncate=False)

spark.stop()
