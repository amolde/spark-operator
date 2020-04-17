import os
from pyspark import SparkConf, SparkContext, sql
from pyspark.sql.functions import first

if __name__ == '__main__':

  conf = SparkConf().setAppName("CommonApp-to-S3")

  sc = SparkContext(conf=conf)
  spark = sql.SparkSession(sc)

  connectionProperties = {
    "user" : os.environ.get('ADMITWARE_USERNAME'),
    "password" : os.environ.get('ADMITWARE_PASSWORD'),
    "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
  }
  jdbcUrl="jdbc:sqlserver://{}:{};database={}".format(os.environ.get('ADMITWARE_HOST'), os.environ.get('ADMITWARE_PORT'), os.environ.get('ADMITWARE_DATABASE'))
  query_table = os.environ.get('ADMITWARE_TABLE')

  s3_uri = 's3a://{}'.format(os.environ.get('S3_FOLDER_NAME'))

  jdbc_query = "select common_app_id, fieldname, fieldvalue from CommonAppLong where common_app_id in (select c.common_app_id from CommonApp c, neucase n where c.common_app_id in ('14101098', '14140102', '14386433') and n.AWID = c.awid and n.termyear = '2019')"
  jdbc_table = "(" + jdbc_query + ") base_tables_alias"
  
  # partition_column = 'common_app_id'
  # lower_bound = 14101098
  # upper_bound = 22648861
  # num_partitions=10


  df = spark.read.jdbc( \
    url=jdbcUrl, \
    table=jdbc_table, \
      # column=partition_column, \
      # lowerBound=lower_bound, \
      # upperBound=upper_bound, \
      # numPartitions=num_partitions, \
      predicates = [\
          "common_app_ID between '14101098' and '14956098'", \
          "common_app_ID between '14956098' and '15811098'", \
          "common_app_ID between '15811098' and '16666098'", \
          "common_app_ID between '16666098' and '17521098'", \
          "common_app_ID between '17521098' and '18376098'", \
          "common_app_ID between '18376098' and '19231098'", \
          "common_app_ID between '19231098' and '20086098'", \
          "common_app_ID between '20086098' and '20941098'", \
          "common_app_ID between '20941098' and '21796098'", \
          "common_app_ID between '21796098' and '22651098'" \
      ], \
      properties=connectionProperties \
    ).groupby('common_app_ID').pivot('FieldName').agg(first("FieldValue"))

  from pyspark.sql.functions import lower
  cols_new = []
  seen = set()
  for c in df.columns:
    cols_new.append('{}_dup'.format(c) if c.lower() in seen else c)
    seen.add(c.lower())

  df2 = df.toDF(*cols_new)

  df2.write.parquet(s3_uri)
  spark.stop()