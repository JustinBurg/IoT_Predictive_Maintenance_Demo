'''
Bulk convert XML to CSV Single Partition
Author:  Justin Brandenburg, Data Scientist @ MapR Data Technologies


In Sandbox:
- upload zip file into /user/user01 using Hue
- zip file gets unzipped, rename file to rw_XML_train

In Sandbox as user01 at command line:

Go into the rw_XML_train folder
[user01@maprdemo ~]$ cd rw_XML_train

Count number of files:
[user01@maprdemo rw_XML_train]$ ls -1 | wc –

The file names have a space in them.  Remove the space with the following:
[user01@maprdemo rw_XML_train]$ find $1 -name "* *.dat" -type f -print0 | while read -d $'\0' f; do mv -v "$f" "${f// /_}"; done

Convert file extension from .dat to .xml:
[user01@maprdemo rw_XML_train]$ for f in *.dat; do mv -- "$f" "${f%.dat}.xml";

Create a new folder :
[user01@maprdemo rw_raw]$ mkdir rw_XML_stream

Move the last 10 xml files from the rw_XML_train location into rw_XML_stream (you can do this in Hue by selecting the box next to the file name and then actions).
These will be used when we deploy our finished model.

To run the code interactively in the Pyspark shell:
[user01@maprdemo ~]$ /opt/mapr/spark/spark-2.1.0/bin/pyspark --packages com.databricks:spark-xml_2.10:0.4.1

To run pyspark script as pyspark job, use the following command:
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




