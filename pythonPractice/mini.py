from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("MiniPipeline").getOrCreate()

df = spark.read.csv("sales.csv", header=True, inferSchema=True)

df_with_tax = df.withColumn("tax", col("amount") * 0.1)

df_with_category = df_with_tax.withColumn(
    "category",
    when(col("amount") > 1000, "High").otherwise("Low")
)

result = df_with_category.filter(
    (col("category") == "High") & (col("region") == "North")
).orderBy(col("amount").desc())

result.show()

result.write.mode("overwrite").csv("output_pipeline", header=True)

spark.stop()
