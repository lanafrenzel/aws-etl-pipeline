import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Get job parameters
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'raw_bucket',
    'clean_bucket',
    'raw_prefix',
    'clean_prefix'
])

# initialize Spark/Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# build S3 paths from parameters
raw_path = f"s3://{args['raw_bucket']}/{args['raw_prefix']}"
clean_path = f"s3://{args['clean_bucket']}/{args['clean_prefix']}"

print(f"Reading from: {raw_path}")
print(f"Writing to: {clean_path}")

try:
    # read raw JSON data
    df_raw = spark.read.json(raw_path)
    
    # flatten data
    df = df_raw.select(explode("data").alias("record")).select("record.*")
    
    # cast columns to appropriate types
    numeric_cols = [
        'open', 'high', 'low', 'close', 'volume', 'adj_high', 'adj_low', 
        'adj_close', 'adj_open', 'adj_volume', 'split_factor', 'dividend'
    ]
    
    for col in numeric_cols:
        df = df.withColumn(col, df[col].cast(FloatType()))
    
    # convert date to timestamp
    df = df.withColumn('date', to_timestamp('date', "yyyy-MM-dd'T'HH:mm:ssZ"))
    
    # add calculated columns
    df = df.withColumn('daily_return', (col('close') - col('open')) / col('open')) \
           .withColumn('is_dividend_day', (col('dividend') > 0).cast(BooleanType()))
    
    # add partition columns
    df = df.withColumn('year', year('date')) \
           .withColumn('month', month('date'))
    
    # sort data
    df_clean = df.sort('symbol', 'date')
    
    # write as partitioned parquet
    df_clean.write.mode('overwrite') \
        .partitionBy('symbol', 'year', 'month') \
        .parquet(clean_path)
    
    print(f"Successfully processed and wrote data to {clean_path}")
    
except Exception as e:
    print(f"Job failed with error: {str(e)}")
    raise e
finally:
    job.commit()
