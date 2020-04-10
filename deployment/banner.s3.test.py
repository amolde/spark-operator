import os
from pyspark import SparkConf, SparkContext, sql

if __name__ == '__main__':

  conf = SparkConf().setAppName("Banner-S3-Test")

  sc = SparkContext(conf=conf)
  spark = sql.SparkSession(sc)

  connectionProperties = {
    "user" : os.environ.get('BANNER_USERNAME'),
    "password" : os.environ.get('BANNER_PASSWORD'),
    "driver" : "oracle.jdbc.driver.OracleDriver"
  }
  jdbcUrl=f"jdbc:oracle:thin:@{os.environ.get('BANNER_HOST')}:{os.environ.get('BANNER_PORT')}:{os.environ.get('BANNER_DATABASE')}"
  query_table = os.environ.get('BANNER_TABLE')

  s3_uri = 's3a://{}'.format(os.environ.get('S3_FOLDER_NAME'))

  jdbc_query = os.environ.get('BANNER_QUERY')
  jdbc_table = "(" + jdbc_query + ") base_tables_alias"

  df = spark.read.jdbc( \
    url=jdbcUrl, \
    table=jdbc_table, \
      numPartitions = 1, \
      properties=connectionProperties \
    )

  df.write.parquet(s3_uri)
  spark.stop()