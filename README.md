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

Once the sandbox is up and running, install Anaconda Python:
https://community.mapr.com/community/exchange/blog/2017/07/18/setting-up-jupyter-notebook-for-spark-210-and-python
(note, instead of installing miniconda, replace with
wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh)

## Author: 
Justin Brandenburg 
Data Scientist, MapR Data Technologies

## Acknowledgements: 
Mike Aube 
Solutions Engineer - MapR Federal, MapR Data TecOverview:

 

Challenge: S 
Data: 2,013 .dat files that, when unpackaged, were xml format




