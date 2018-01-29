'''
Ingest XML Files into MapR Streams
Author:  Justin Brandenburg, Data Scientist
Email:   jbrandenburg@mapr.com

Requirements: Python 3.5
If not installed, this demo will not run

This assumes that the raw .dat files have been converted to the proper xml format and the file names have spaces removed.
[user01@maprdemo rw_raw]$ mkdir rw_XML_stream
Move the last 10 xml files from the rw_XML_train location into rw_XML_stream (you can do this in Hue)

Run from the command line with the following 
[user01@maprdemo ~]$ python Sensor_XML2MaprStreams_producer.py
'''

print ("Importing dependencies....")
import mapr_kafka_rest
import random
import time
import datetime
import os
import xml.etree.ElementTree as ET
import pandas as pd
import glob
print("Import complete.\n") 


# Set up some reusable values
sensor_topic_name  = '/user/user01/iot_stream:sensor_record'
path = '/user/user01/rw_XML_stream'

def xml2df(xml_file):
    root = ET.XML(xml_file) # element tree
    all_records = [] #This is our record list which we will convert into a dataframe
    for i, child in enumerate(root): #Begin looping through our root tree
        record = {} #Place holder for our record
        for subchild in child: #iterate through the subchildren to user-agent, Ex: ID, String, Description.
            record[subchild.tag] = subchild.text #Extract the text create a new dictionary key, value pair
            all_records.append(record) #Append this record to all_records.
    return pd.DataFrame(all_records) #return records as DataFrame

records = 0
for xml_filename in glob.glob(path+"/*.xml"):
#for xml_filename in glob.glob(path+"/2016_1_0_12_20160722_1437048553.xml"):
    f = open(xml_filename).read()
    df = xml2df(f).drop_duplicates().reset_index(drop=True).sort_values(['TimeStamp'], ascending=True)
    df['TagValue']=df.TagValue.astype(float).fillna(0)
    #df['TimeStamp']=pd.to_datetime(df['TimeStamp'])
    df = df.pivot(index='TimeStamp', columns='TagName', values='TagValue').fillna(0).rename_axis(None, axis=1).reset_index()
    df['filename'] = xml_filename
    #df = df[df["::[scararobot]speed"] != 0]
    #df['TimeStamp'] = str(datetime.datetime.df['TimeStamp'])

    for index,row in df.iterrows():
        records +=1
        sensor_df_record = {}
        sensor_df_record['filename']=row["filename"]
        sensor_df_record['TimeStamp']=row['TimeStamp']
        sensor_df_record['::[scararobot]Ax_J1.ActualPosition']=row['::[scararobot]Ax_J1.ActualPosition']
        sensor_df_record['::[scararobot]Ax_J1.PositionCommand']=row['::[scararobot]Ax_J1.PositionCommand']
        sensor_df_record['::[scararobot]Ax_J1.PositionError']=row['::[scararobot]Ax_J1.PositionError']
        sensor_df_record['::[scararobot]Ax_J1.TorqueCommand']=row['::[scararobot]Ax_J1.TorqueCommand']
        sensor_df_record['::[scararobot]Ax_J1.TorqueFeedback']=row['::[scararobot]Ax_J1.TorqueFeedback']
        sensor_df_record['::[scararobot]Ax_J2.ActualPosition']=row['::[scararobot]Ax_J2.ActualPosition']
        sensor_df_record['::[scararobot]Ax_J2.PositionCommand']=row['::[scararobot]Ax_J2.PositionCommand']
        sensor_df_record['::[scararobot]Ax_J2.PositionError']=row['::[scararobot]Ax_J2.PositionError']
        sensor_df_record['::[scararobot]Ax_J2.TorqueCommand']=row['::[scararobot]Ax_J2.TorqueCommand']
        sensor_df_record['::[scararobot]Ax_J2.TorqueFeedback']=row['::[scararobot]Ax_J2.TorqueFeedback']
        sensor_df_record['::[scararobot]Ax_J3.ActualPosition']=row['::[scararobot]Ax_J3.ActualPosition']
        sensor_df_record['::[scararobot]Ax_J3.PositionCommand']=row['::[scararobot]Ax_J3.PositionCommand']
        sensor_df_record['::[scararobot]Ax_J3.PositionError']=row['::[scararobot]Ax_J3.PositionError']
        sensor_df_record['::[scararobot]Ax_J3.TorqueCommand']=row['::[scararobot]Ax_J3.TorqueCommand']
        sensor_df_record['::[scararobot]Ax_J3.TorqueFeedback']=row['::[scararobot]Ax_J3.TorqueFeedback']
        sensor_df_record['::[scararobot]Ax_J6.ActualPosition']=row['::[scararobot]Ax_J6.ActualPosition']
        sensor_df_record['::[scararobot]Ax_J6.PositionCommand']=row['::[scararobot]Ax_J6.PositionCommand']
        sensor_df_record['::[scararobot]Ax_J6.PositionError']=row['::[scararobot]Ax_J6.PositionError']
        sensor_df_record['::[scararobot]Ax_J6.TorqueCommand']=row['::[scararobot]Ax_J6.TorqueCommand']
        sensor_df_record['::[scararobot]Ax_J6.TorqueFeedback']=row['::[scararobot]Ax_J6.TorqueFeedback']
        sensor_df_record['::[scararobot]CS_Cartesian.ActualPosition[0]']=row['::[scararobot]CS_Cartesian.ActualPosition[0]']
        sensor_df_record['::[scararobot]CS_Cartesian.ActualPosition[1]']=row['::[scararobot]CS_Cartesian.ActualPosition[1]']
        sensor_df_record['::[scararobot]CS_Cartesian.ActualPosition[2]']=row['::[scararobot]CS_Cartesian.ActualPosition[2]']
        sensor_df_record['::[scararobot]CS_SCARA.ActualPosition[0]']=row['::[scararobot]CS_SCARA.ActualPosition[0]']
        sensor_df_record['::[scararobot]CS_SCARA.ActualPosition[1]']=row['::[scararobot]CS_SCARA.ActualPosition[1]']
        sensor_df_record['::[scararobot]CS_SCARA.ActualPosition[2]']=row['::[scararobot]CS_SCARA.ActualPosition[2]']
        sensor_df_record['::[scararobot]ScanTimeAverage']=row['::[scararobot]ScanTimeAverage']
        sensor_df_record['::[scararobot]speed']=row['::[scararobot]speed']


        response = mapr_kafka_rest.post_topic_message(sensor_topic_name, sensor_df_record)
        if (response.status_code == 200):
            print("POSTED: " + str(sensor_df_record))
        else:
            print('ERROR: %d "%s"' % (response.status_code,response.reason))
        time.sleep(0.25)

print("\nExecuted parsing and streaming "+ str(records) + " Timestamps!")

