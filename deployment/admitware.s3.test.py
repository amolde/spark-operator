import os
from pyspark import SparkConf, SparkContext, sql

if __name__ == '__main__':

  conf = SparkConf().setAppName("Admitware-S3-Test")

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

  jdbc_query = "select top(10) StudentDocID, ACAdmitLetterId, NUID, FWID, Term, TermYear, AppID, DocType, LetterDecisionType  from {}".format(query_table)
  jdbc_table = "(" + jdbc_query + ") base_tables_alias"
  # partition_column = 'StudentDocID' and 'ACAdmitLetterId'

  df = spark.read.jdbc( \
    url=jdbcUrl, \
    table=jdbc_table, \
      # column=partition_column, \ # maximal number of concurrent JDBC connections
      # lowerBound=1, \
      # upperBound=100000, \
      # numPartitions=100, \
      # predicates = ["TABLE_TYPE != 'BASE TABLE'", "TABLE_TYPE = 'BASE TABLE'" ], \
      numPartitions = 1, \
      properties=connectionProperties \
    )

  df.write.parquet(s3_uri)
  spark.stop()