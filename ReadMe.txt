=============================================================================
                            IoT Sensor Demo
=============================================================================

Author:  Justin Brandenburg, Data Scientist
Email:   jbrandenburg@mapr.com

Special Assistance From:
Michael F. Aube, Solutions Engineer - Federal
maube@mapr.com
=============================================================================

Here are the files you should have as part of this package:
-----------------------------------------------------------------------------
 ReadMe.txt                                  (this file)
 Anaconda_Python_Install_Instructions.docx   Word document that has installation instructions
 mapr_kafka_rest.py                          A module that wraps Kafka REST API for POST and GET 
 Sensor_ETLsparksubmit.py                    Pyspark executable that performs bulk xml to csv conversion
 Sensor_Historical_Data_Analysis.py          A module performing data exploration and model construction on historical data
 Sensor_XML2MaprStreams_producer.py          A module that ingests xml files into MapR Streams
 Stream_IoT_Prediction_Dashboard_plotly.py   A module that reads MapR Streams and applies a Deep Learning Model and Visualization

=============================================================================
                       *** PLEASE NOTE: *** 

The Python files included in this demo package assume that you have installed
Python 3.5.2 AND the "Requests HTTP Library for Python".
 
Refer to the word document "Anaconda_Python_Install_Instructions.docx" to 
install Python 3.5.2 from Continuum Analytics
=============================================================================
1. Create a new MapR Sandbox VM inside VirtualBox by importing the file named:
   
   MapR-Sandbox-For-Hadoop-5.2.1.ova
   
   
2. Before you start your new "Sandbox" VM, add the following line to
   the Port Forwarding rules for the NAT network interface.  If you are
   running the gateway on a different port, please substitute your port
   number for '8082' below.  Add jupyter to this as well.   
   -----------------------------------------------------------------------------
   |    Name         Protocol  Host IP       Host Port   Guest IP   Guest Port |
   -----------------------------------------------------------------------------
   Kafka_REST        TCP       127.0.0.1     8082                   8082
   jupyter           TCP       127.0.0.1     9999                   9999

3. Start your new Sendbox VM, and let it come up all the way.


4. Login as the ‘root’ user, install the Kafka REST Gateway, set the flush timeout 
   for the Kafka REST gateway buffer, and then restart the Warden service:

   $ ssh -p 2222 root@localhost
   password: mapr

   [root@maprdemo ~]# yum install mapr-kafka-rest
   [root@maprdemo ~]# echo 'streams.buffer.max.time.ms=100' >> /opt/mapr/kafka-rest/kafka-rest-2.0.1/config/kafka-rest.properties
   [root@maprdemo ~]# service mapr-warden restart
   [root@maprdemo ~]# exit

5. Login as the 'user01' user, create the MapR Stream and Topic for this demo:

   $ ssh -p 2222 user01@localhost
   password: mapr

   [user01@maprdemo ~]$ maprcli stream create -path /user/user01/iot_stream -produceperm p -consumeperm p -topicperm p
   [user01@maprdemo ~]$ maprcli stream topic create -path /user/user01/iot_stream -topic sensor_record
   
   -------------------------------------------------------------------------------
   FYI:  If you want to delete the topic to start over, issue this command:
   [user01@maprdemo ~]$ maprcli stream topic delete -path /user/user01/iot_stream -topic sensor_record

   Use the following command to list all of the topics within a given stream:
   [user01@maprdemo ~]$ curl -X GET http://localhost:8082/streams/%2Fuser%2Fuser01%2Fiot_stream/topics
   -------------------------------------------------------------------------------

6. Now use scp or vi to copy the following Python files into your 
   Sandbox VM at '/user/user01'.

=============================================================================
                       *** Plotly Visualization *** 
For the visualization:
First, go to https://plot.ly/ and set up an account.  Once you have set up an account, go to your account settings and on the left you will see a menu selection for API key.  Click that and then "Regenerate Key".   Then set up two Streaming API tokens.  Once this is completed  you need to install the plotly package in the Sandbox and then set up your credentials.  In the sandbox do the following:

[user01@maprdemo ~]$ pip install plotly

[user01@maprdemo ~]$ vi ~/.plotly/.credentials

add in stream tokens,username and api-key.  To view your visualization, click on the My Files tab on the plotly website and then "view". 















