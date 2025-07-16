from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("CustomerPipeline") \
    .getOrCreate()
# Read the CSV into a DataFrame
customers_df = spark.read.csv("customers.csv", header=True, inferSchema=True)

# Show data
customers_df.show()
