'''
Bulk convert XML to CSV Single Partition
Author:  Justin Brandenburg, Data Scientist
Email:   jbrandenburg@mapr.com

Requirements: change Pyspark python to Python 3.5

In Sandbox:
- upload zip file into /user/user01 using Hue
- zip file gets unzipped, rename file to rw_raw

In Sandbox as user01 at command line:
[user01@maprdemo ~]$ cd rw_raw
[user01@maprdemo rw_raw]$ ls -1 | wc -
[user01@maprdemo ]$ mkdir rw_XML_train
[user01@maprdemo rw_raw]$ cd ..
- copy raw data to new folder for xml conversion
[user01@maprdemo ~]$ cp -R rw_raw rw_XML_train/
- delete rw_raw in hue to clear up space 
- convert to xml
[user01@maprdemo ~]$ cd rw_XML_train
[user01@maprdemo rw_XML_train]$ find $1 -name "* *.dat" -type f -print0 | while read -d $'\0' f; do mv -v "$f" "${f// /_}"; done
[user01@maprdemo rw_XML_train]$ for f in *.dat; do mv -- "$f" "${f%.dat}.xml";    NOTE: if in ubuntu, put "done" at the end
[user01@maprdemo ~]$ /opt/mapr/spark/spark-2.1.0/bin/spark-submit  --packages com.databricks:spark-xml_2.10:0.4.1 /user/user01/Sensor_ETLsparksubmit.py
'''


#PYSPARK Executable script
#import libraries
print ("Importing dependencies....")
import sys
import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, IntegerType, StructType, StructField, DoubleType, FloatType, DateType, TimestampType
from pyspark.sql.functions import date_format, col, desc, udf, from_unixtime, unix_timestamp, date_sub, date_add, last_day
import time
print("Import complete.\n") 

def xmlConvert(spark):

		etl_time = time.time()
		df = spark.read.format('com.databricks.spark.xml').options(rowTag='HistoricalTextData').load('maprfs:///user/user01/rw_XML_train')
		df = df.withColumn("TimeStamp", df["TimeStamp"].cast("timestamp")).groupBy("TimeStamp").pivot("TagName").sum("TagValue").na.fill(0)
		df.repartition(1).write.csv("maprfs:///user/user01/rw_etl.csv", header=True, sep=",")
		print ("Time taken to do xml transformation: --- %s seconds ---" % (time.time() - etl_time))

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName('XML ETL') \
        .getOrCreate()

    print('Session created')

    try:
        xmlConvert(spark)

    finally:
    	spark.stop()




