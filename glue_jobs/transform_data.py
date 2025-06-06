# Glue Interactive Session Configuration
%idle_timeout 2880
%glue_version 3.0
%worker_type G.1X
%number_of_workers 5

# Set your environment variables here
import os

os.environ['RAW_BUCKET'] = 'your-bucket'
os.environ['CLEAN_BUCKET'] = 'your-bucket'
os.environ['RAW_PREFIX'] = 'raw/'
os.environ['CLEAN_PREFIX'] = 'clean/'

# Main part
import sys
import traceback
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Spark context
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Configuration 
RAW_BUCKET = os.environ.get('RAW_BUCKET')
CLEAN_BUCKET = os.environ.get('CLEAN_BUCKET')
RAW_PREFIX = os.environ.get('RAW_PREFIX', 'raw/')
CLEAN_PREFIX = os.environ.get('CLEAN_PREFIX', 'clean/')

# Validate required configuration
if not RAW_BUCKET:
    raise ValueError("RAW_BUCKET environment variable is required")
if not CLEAN_BUCKET:
    raise ValueError("CLEAN_BUCKET environment variable is required")

# Build S3 paths
raw_path = f"s3://{RAW_BUCKET}/{RAW_PREFIX}"
clean_path = f"s3://{CLEAN_BUCKET}/{CLEAN_PREFIX}"

print(f"Reading from: {raw_path}")
print(f"Writing to: {clean_path}")

def process_stock_data():
    """
    Process raw stock data from S3, perform transformations, and save as partitioned Parquet.
    
    Returns:
        bool: True if processing successful, False otherwise
    """
    try:
        # Read raw JSON data from S3
        print("Reading raw JSON data")
        df_raw = spark.read.json(raw_path)
        
        # Validate data exists
        if df_raw.count() == 0:
            raise Exception("No data found in raw path")
        
        # Flatten nested JSON structure
        print("Flattening data structure")
        df = df_raw.select(explode("data").alias("record")).select("record.*")
        
        # Define numeric columns for type casting
        numeric_cols = [
            'open', 'high', 'low', 'close', 'volume', 'adj_high', 'adj_low', 
            'adj_close', 'adj_open', 'adj_volume', 'split_factor', 'dividend'
        ]
        
        # Cast numeric columns to FloatType
        print("Casting numeric columns")
        for col_name in numeric_cols:
            if col_name in df.columns:
                df = df.withColumn(col_name, df[col_name].cast(FloatType()))
        
        # Parse date column to timestamp
        print("Processing date column")
        df = df.withColumn('date', to_timestamp('date', "yyyy-MM-dd'T'HH:mm:ssZ"))
        
        # Add calculated columns
        print("Adding calculated columns")
        df = df.withColumn('daily_return', 
                          when(col('open') != 0, (col('close') - col('open')) / col('open'))
                          .otherwise(0)) \
               .withColumn('is_dividend_day', (col('dividend') > 0).cast(BooleanType()))
        
        # Add partitioning columns  
        print("Adding partition columns")
        df = df.withColumn('year', year('date')) \
               .withColumn('month', month('date'))
        
        # Sort data for optimal partitioning
        print("Sorting data")
        df_clean = df.sort('symbol', 'date')
        
        # Get record count before showing sample
        record_count = df_clean.count()
        
        # Show sample for verification
        print("Sample of processed data:")
        df_clean.show(5, truncate=False)
        
        # Write partitioned Parquet to S3
        print("Writing partitioned Parquet files")
        df_clean.write.mode('overwrite') \
            .partitionBy('symbol', 'year', 'month') \
            .option('compression', 'snappy') \
            .parquet(clean_path)
        
        print(f"Successfully processed {record_count:,} records")
        print(f"Data written to: {clean_path}")
        
        return True
    
    except Exception as e:
        print(f"Processing failed: {str(e)}")
        traceback.print_exc() 
        return False


# Execute transformation
if __name__ == "__main__":
    success = process_stock_data()
    
    if success:
        print("ETL pipeline completed successfully!")
    else:
        print("ETL pipeline failed!")
        sys.exit(1)
