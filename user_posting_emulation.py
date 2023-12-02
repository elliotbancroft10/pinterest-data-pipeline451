import requests
from datetime import datetime
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from kafka import KafkaConsumer

random.seed(100)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

# Number of posts to make, 1 post indicates 1 post of pin, geo and user data
post_limit = 1

topic_dict = {'12869112c9e5.pin':'Pinterest Data', 
              '12869112c9e5.geo':'Geographic Data',
              '12869112c9e5.user':'User Data'}

def send_to_kafka(data, topic_name):
    invoke_url = f"https://x84i29wg1c.execute-api.us-east-1.amazonaws.com/12869112c9e5/topics/{topic_name}"
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    #'Content-Type': 'application/vnd.kafka.json.v2+json'
    if topic_name == '12869112c9e5.pin':
        corrected_data = data
    else:
        corrected_data = {key.replace('ind', 'index'): value for key, value in data.items()}
    payload = json.dumps({
        "topic": topic_dict[topic_name],
        "payload":[corrected_data]}, default=str)#, cls=DateTimeEncoder) 
    response = requests.post(invoke_url, headers=headers, data=payload)
    print(response.status_code)
    print(payload)

    #bootstrap_servers = 'b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098'
    #consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers)
    #for message in consumer:
    #    print(f"Received message: {message.value}")

def run_infinite_post_data_loop():
    post_counter = 0

    while post_counter < post_limit:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            send_to_kafka(pin_result, '12869112c9e5.pin')
            send_to_kafka(geo_result, '12869112c9e5.geo')
            send_to_kafka(user_result, '12869112c9e5.user')

            post_counter += 1 
  

if __name__ == "__main__":
    print('Working')
    run_infinite_post_data_loop()

print(f"{post_limit} results posted successfully!")
    

