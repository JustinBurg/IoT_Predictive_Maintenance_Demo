Author: Justin Brandenburg, Data Scientist, MapR Data Technologies

Special Assistance From: Mike Aube, Solutions Engineer - MapR Federal, MapR Data Techologies

This is a demo that utilizes the MapR Converged Data Platform, Pyspark, TensorFlow and Python 3.5 for predicting the next time period value in a time series on data from an IoT device.  This is particularly useful for manufacturing and industry 4.0 where sensors are attached to components sending data back for real time monitoring.  This demo takes real time monitoring and enhances with it with prediction capabilities that can generate alerts when the prediction exceeds a threshold of normal behavior. 

To get started, download the MapR Sandbox and install in Virtual Box:
https://maprdocs.mapr.com/52/SandboxHadoop/t_install_sandbox_vbox.html

Once the sandbox is up and running, install Anaconda Python:
https://community.mapr.com/community/exchange/blog/2017/07/18/setting-up-jupyter-notebook-for-spark-210-and-python
(note, instead of installing miniconda, replace with
wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh)
