# IoT Predictive Maintenance using Recurrent Neural Networks

The idea behind predictive maintenance is that the failure patterns of various types of equipment are predictable. If we can predict when a piece of hardware will fail accurately, and replace that component before it fails, we can achieve much higher levels of operational efficiency.

With many devices now including sensor data and other components that send diagnosis reports, predictive maintenance using big data becomes increasingly more accurate and effective.

This is a demo that utilizes the MapR Converged Data Platform, Pyspark, TensorFlow and Python 3.5 for predicting the next time period value in a time series on data from an IoT device.  This is particularly useful for manufacturing and industry 4.0 where sensors are attached to components sending data back for real time monitoring.  This demo takes real time monitoring and enhances with it with prediction capabilities that can generate alerts when the prediction exceeds a threshold of normal behavior.

## What are we working with?
Sensor attached to a automated manufacturing device capture position and calibration at each time stamp.  Sensor is capturing real time data on the device and its current health.  The data is stored for historical analysis to identify trends and patterns to determine if any devices need to be taken out of production for health checks and maintenance.

## Data
2,013 .dat files that, when unpackaged, were xml format

## What you need
To get started, download the MapR Sandbox and install in Virtual Box:
https://maprdocs.mapr.com/52/SandboxHadoop/t_install_sandbox_vbox.html

Before you start your new "Sandbox" VM, add the following line to
the Port Forwarding rules for the NAT network interface.  If you are
running the gateway on a different port, please substitute your port
number for '8082' below.  Add jupyter to this as well.   
Kafka_REST TCP 127.0.0.1 8082 8082
jupyter TCP 127.0.0.1 9999 9999

### Login as the ‘root’ user, install the Kafka REST Gateway

Set the flush timeout for the Kafka REST gateway buffer, and then restart the Warden service:
$ ssh -p 2222 root@localhost

password: mapr

[root@maprdemo ~]# yum install mapr-kafka-rest

[root@maprdemo ~]# echo 'streams.buffer.max.time.ms=100' >> /opt/mapr/kafka-rest/kafka-rest-2.0.1/config/kafka-rest.properties

[root@maprdemo ~]# service mapr-warden restart

[root@maprdemo ~]# exit

### Login as the 'user01' user, create the MapR Stream and Topic for this demo:
$ ssh -p 2222 user01@localhost

password: mapr

[user01@maprdemo ~]$ maprcli stream create -path /user/user01/iot_stream -produceperm p -consumeperm p -topicperm p

[user01@maprdemo ~]$ maprcli stream topic create -path /user/user01/iot_stream -topic sensor_record

Now use scp or vi to copy the following Python files into your Sandbox VM at '/user/user01'.

Install Anaconda Python:
https://community.mapr.com/community/exchange/blog/2017/07/18/setting-up-jupyter-notebook-for-spark-210-and-python
(note, instead of installing miniconda, replace with
"wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh")
The Python files included in this demo package assume that you have installed
Python 3.5.2 AND the "Requests HTTP Library for Python".

### For the visualization:
First, go to https://plot.ly/ and set up an account.  Once you have set up an account, go to your account settings and on the left you will see a menu selection for API key.  Click that and then "Regenerate Key".   Then set up two Streaming API tokens.  Once this is completed  you need to install the plotly package in the Sandbox and then set up your credentials.  In the sandbox do the following:

[user01@maprdemo ~]$ pip install plotly

[user01@maprdemo ~]$ vi ~/.plotly/.credentials

add in stream tokens,username and api-key.  To view your visualization, click on the My Files tab on the plotly website and then "view". 



## Author: 
Justin Brandenburg 
Data Scientist, MapR Data Technologies

## Acknowledgements: 
Mike Aube 
Solutions Engineer - MapR Federal, MapR Data Technologies
