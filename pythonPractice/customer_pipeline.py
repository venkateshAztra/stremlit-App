# 1️⃣ Create Spark session
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("CustomerPipeline") \
    .getOrCreate()