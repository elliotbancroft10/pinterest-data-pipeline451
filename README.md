# Pinterest Data Pipeline
### An AICore Data Engineering Project

## Contents
1. [Project Synopsis](#project_synopsis)
2. [Project Resources](#project_resources)
3. [Data](#data)
4. [Setup and Usage](#setup_and_usage)
5. [File Structure](#file_structure)

## Project Synopsis <a name="project_synopsis"></a>
This project retrieves pinterest, user and geographical data from an RDS dataset. The data is then stored in a DataBricks mounted S3 bucket.

To transfer the data into the S3 bucket, an API was created using AWS API Gateway, which in turn allows the data to be sent via the MSK cluster, to the connected S3 bucket using the IAM MSK authentication package.

Once the 3 bucket had been mounted to DataBricks, a series of queries and analysis were performed and can be found in pinterest_df_manipulation.ipynb.

## Project Resources <a name="project_resources"></a>
* [Apache Kafka](https://kafka.apache.org/documentation/)
>Apache Kafka is an open-source distributed event streaming platform that allows you to publish and subscribe to streams of records, store and process those records in a fault-tolerant manner, and integrate Kafka with various data systems.

* [Apache Spark](https://spark.apache.org/docs/latest/)
>Apache Spark is an open-source, distributed computing system that provides a fast and general-purpose cluster-computing framework for big data processing and analytics.

* [Confluent REST Proxy](https://docs.confluent.io/platform/current/kafka-rest/index.html)
>Confluent REST Proxy is a component within the Confluent Platform that provides a RESTful interface for interacting with Apache Kafka, simplifying the integration of Kafka with applications through HTTP-based communication.

* [Databricks](https://docs.databricks.com/en/index.html)
>Databricks is a unified analytics platform that combines big data processing and machine learning capabilities, providing an integrated environment for data scientists, engineers, and analysts to collaboratively work on data-intensive projects.

* [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
>PySpark is the Python API for Apache Spark, offering a high-level interface to efficiently process large-scale data across distributed computing clusters.

### AWS Resources
* [AWS MSK](https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html)
>Amazon MSK (Managed Streaming for Apache Kafka) is a fully managed service that simplifies the deployment, operation, and scaling of Apache Kafka clusters on AWS.

* [AWS MSK Connect](https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect.html)
>AWS MSK Connect is a feature that enables seamless integration between Apache Kafka clusters managed by Amazon MSK and other AWS services, allowing for easy data streaming and event-driven application development.

* [AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
>AWS API Gateway is a fully managed service that enables developers to create, publish, maintain, monitor, and secure APIs at any scale, facilitating the creation of robust and scalable backend services.

* [AWS Managed Workflows for Apache Airflow (MWAA)](https://docs.aws.amazon.com/mwaa/)
>AWS MWAA (Managed Workflows for Apache Airflow) is a fully managed service that simplifies the deployment and operation of Apache Airflow, providing a scalable and serverless environment for orchestrating and scheduling data workflows.

* [AWS Kinesis](https://docs.aws.amazon.com/kinesis/)
>AWS Kinesis is a cloud service that enables real-time processing of streaming data at scale, offering capabilities for ingestion, processing, and analysis of large volumes of data from various sources.

## Data <a name="data"></a>
Data aimed at replicating the type of data Pinterest Data Engineers will deal with was generated in a stream using the [user_posting_emulation.py](user_posting_emulation.py) script. 

In this case, the script connects to an AWS RDS database using an SQLAlchemy engine. The database contains three tables relating to each post in the stream. After the data has been extracted from RDS and formatted in a dictionary, it looks like the below:

pinterest_data:
```
{"records": [{"value": {"index": 2604, "unique_id": "087b0fa9-f901-4262-aa0a-6caf234d1b35", "title": "75+ Neutral Christmas Home Decor for the Holiday Season in Farmhouse Style using Earth Tones Modern", "description": "My favorite 75+ Neutral Christmas Home Decor for decorating your house during the Holiday Season in earth tones and a farmhouse, rustic style all winter. I love this modern, sim\u2026\u00a0", "poster_name": "Everyday Wholesome", "follower_count": "31k", "tag_list": "Colorful Christmas Decorations,Colorful Christmas Tree,Christmas Centerpieces,Christmas Colors,Xmas Colors,Winter Decorations,Christmas Trends,Christmas Inspiration,Christmas Home", "is_image_or_video": "image", "image_src": "https://i.pinimg.com/originals/86/84/39/868439dd894969e3abd6a2a8a9fe1e9c.jpg", "downloaded": 1, "save_location": "Local save in /data/christmas", "category": "christmas"}}]}
```

geolocation_data:
```
{"records": [{"value": {"index": 223, "timestamp": "2018-12-07T07:30:40", "latitude": 1.15509, "longitude": -118.397, "country": "Isle of Man"}}]}
```

user_data:
```
{"records": [{"value": {"index": 223, "first_name": "Melanie", "last_name": "Hill", "age": 51, "date_joined": "2016-10-09T14:47:51"}}]}
```

## Setup and Usage <a name="setup_and_usage"></a>

## File Structure <a name="file_structure"></a>
