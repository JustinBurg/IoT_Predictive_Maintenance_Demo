"""
The mapr_kafka_rest module implements a simplified Python wrapper for selected
calls in the MapR Kafka REST API.

Most of the actual 'boiler plate' details for these REST API calls have been 
abstracted out of the Python functions as parameters with default values.
This allows users of this module to focus on the message and topic details.  

"""

import requests

def post_topic_message(
        a_mapr_topic,      # looks like: '/apps/iot_stream:sensor_json',
        a_message,         # usually JSON as a Python dictionary...  
        a_kafka_rest_url = 'http://localhost:8082/topics/',
        a_content_type   = 'application/vnd.kafka.json.v1+json' ) :
    """

    POSTs a_message to a_mapr_topic via the MapR Kafka REST API Gateway.

    --------------------
    Function Parameters:
    --------------------

    a_mapr_topic     - the full name of the destination MapR Streams topic.  
                       An example is:  '/apps/iot_stream:sensor_json'.

    a_message        - the message to be published on a_mapr_topic

    a_kafka_rest_url - OPTIONAL - The URL of the Kafka REST gateway.
                       The default value is: 'http://localhost:8082/topics/'.

    a_content_type   - OPTIONAL - the content type of a_message.
                       The default value is: 'application/vnd.kafka.json.v1+json'.  
    """
 	
    # assemble the full JSON for this record
    json = {}
    json['value'] = a_message
    ## json-> { 'value': {'mac':'18-FE-34-17-BF-C2', 'amplitude':452109} }
    
    # add this record to a list of records (it is "possible" to send N messages per POST)
    records = []
    records.append(json)
    ## records-> [ {'value': {'mac':'18-FE-34-17-BF-C2', 'amplitude':452109}} ]
    
    # construct the requests 'POST' payload
    payload = {}
    payload['records'] = records
    ## payload-> { 'records': [{'value': {'mac':'18-FE-34-17-BF-C2', 'amplitude':452109}}] }
    
    # URL-Encode the topic name: / becomes %2F and : becomes %3A
    encoded_mapr_topic = a_mapr_topic.replace('/','%2F').replace(':','%3A')
    url = a_kafka_rest_url + encoded_mapr_topic
	
    headers={}
    headers['Content-Type'] = a_content_type
	
    # Now send the HTTP POST request to the Kafka REST Gateway
    response = requests.post(url, json=payload, headers=headers)
    # print("JSON PAYLOAD: " + str(payload))

    return response


def get_topic_message(
        a_mapr_topic_name = '/apps/iot_stream:sensor_json',
        a_topic_partition = 0,
        a_topic_offset    = 1,
        a_kafka_rest_url  = 'http://localhost:8082/topics/',
        a_content_type    = 'application/vnd.kafka.json.v1+json' ) :
    """

    Returns a single message from a_mapr_topic_name using a_topic_partition
    number and a_topic offset number via the MapR Kafka REST API Gateway..

    --------------------
    Function parameters:
    --------------------

    a_mapr_topic_name - the complete MapR topic name: <stream-path>:<topic_name>
 
    a_topic_partition - the partion number - default value is 0

    a_topic_offset    - the message offset number - default value is 1

    a_kafka_rest_url  - OPTIONAL - the URL location of the MapR Kafka REST gateway.
                        The default value is: 'http://localhost:8082/topics/'.

    a_content_type    - OPTIONAL - the content type of the message.
                        The default value is: 'application/vnd.kafka.json.v1+json'

    """
# This is an example of a command line "GET" using the MapR Kafka REST gateway:	
# curl -X GET -H "Accept: application/vnd.kafka.json.v1+json" /
# "http://localhost:8082/topics/%2Fapps%2Fiot_stream%3Asensor_json/partitions/0/messages?offset=0&count=1"
    
    # URL-Encode the topic name: / becomes %2F and : becomes %3A
    encoded_mapr_topic = a_mapr_topic_name.replace('/','%2F').replace(':','%3A')

    # Build the complete URL for the GET request 
    url = a_kafka_rest_url + encoded_mapr_topic + '/partitions/' + str(a_topic_partition) + '/messages'
	
    payload = {'offset':a_topic_offset, 'count':1}    # get a single message only
 
    req_headers={'Accept':a_content_type}

    # Now send the HTTP GET request to the Kafka REST Gateway
    response = requests.get(url, params=payload, headers=req_headers)

    if (response.status_code == 200):
        return response.text
    else :
        print('Error: ' + str(response.status_code) )
        print(response.url)
        print(response.headers)
    #
    # End of Function: get_topic_message()
