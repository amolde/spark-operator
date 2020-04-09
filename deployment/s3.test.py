from pyspark import SparkConf, SparkContext, sql

if __name__ == '__main__':
  conf = SparkConf().setAppName("app")
  sc = SparkContext(conf=conf)

  spark = sql.SparkSession \
      .builder \
      .appName("TEST") \
      .getOrCreate()

  sql_context = sql.SQLContext(sc, spark)
  filename = 'admitware/test.parquet4'
  s3_uri = 's3a://nu-data-lake-test/{}'.format(filename)
  print(s3_uri)
  df = sql_context.createDataFrame([('1', '4'), ('2', '5'), ('3', '6')], ["A", "B"])
  df.write.parquet(s3_uri)
  # df.write.parquet("s3a://nu-data-lake-test/admitware/test.parquet",mode="overwrite")

# spark.stop()