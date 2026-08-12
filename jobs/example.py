from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("example").getOrCreate()

data = [("alpha", 1), ("beta", 2), ("gamma", 3)]
df = spark.createDataFrame(data, ["name", "value"])

df.show()

spark.stop()
