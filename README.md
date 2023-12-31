# Pinterest Data Pipeline
>### An AICore Data Engineering Project

## Contents
1. [Project Synopsis](#project_synopsis)
2. [Project Resources](#project_resources)
3. [Data](#data)
4. [Setup and Usage](#setup_and_usage)

## Project Synopsis <a name="project_synopsis"></a>
This project aims to replicate and simplify a system used by Pinterest data engineers to extract, load and real-time posting data, including performing analysis on existing data  using cloud computing infrastructure which theoretically scales to big datasets.

Two separate pipelines are used to process real-time streaming data, including metrics such as popularity of post categories, which could be used for live post recommendations, the other pipeline is used for analyses on historical data, such as account popularity based on age and joining year.

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
### Milestone 3 - Creating Kafka Topics in the EC2 Client
- Create a .pem key file and store it locally
- Connect to the EC2 instance using SSH:
  `ssh -i "your-key-pair-name.pem" ec2-user@your-ec2-instance-public-DNS`
- Install Kafka on your EC2 client machine. Ensure the version is the same version that the MSK cluster is running on
- Install the IAM MSK authentication package on your client EC2 machine to connect to any clusters requiring IAM authentication
- Create an an IAM access role that allows access to the MSK cluster
- Configure the Kafka client to use AWS IAM authentication to the cluster. To do this, you will need to modify the client.properties file as below:
  ```
  # Sets up TLS for encryption and SASL for authN.
  security.protocol = SASL_SSL

  # Identifies the SASL mechanism to use.
  sasl.mechanism = AWS_MSK_IAM

  # Binds SASL client implementation.
  sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="your-ec2-access-role";

  # Encapsulates constructing a SigV4 signature based on extracted credentials.
  # The SASL client bound by "sasl.jaas.config" invokes this class.
  sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
  ```
- To create Kafka topics, the Bootstrap servers string and the Plaintext Apache Zookeeper connection string for the MSK cluster are required
- Then topics can be created using the below command:
  ```
  ./kafka-topics.sh --create --zookeeper "your_bootstrap_server_string" --replication-factor 2 --partitions 1 --topic your_topic_name
  ```

### Milestone 4 - Connecting an S3 Bucket to the Cluster
- On the EC2 client, download the Confluent.io Amazon S3 Connector and copy it to the S3 bucket:
  `wget https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-s3/versions/10.0.3/confluentinc-kafka-connect-s3-10.0.3.zip`
- Create a custom plugin in the MSK Connect console
- Create an MSK connctor, paying attention to the topics.regex field in the connector configuration. Make   sure it has a structure which represents the Kafka topic sturtures previously created. In this case: "your_UserId.*" This will ensure that data going through all the three previously created Kafka topics will get saved to the S3 bucket. When building the connector, make sure to choose the IAM role used for authentication to the MSK cluster in the Access permissions tab

### Milestone 5 - Create an API Gateway to Send Data to the MSK Cluster
- Inside AWS API Gateway, a resource is created that allows a PROXY integration to the API
- The PROXY contains a HTTP ANY method, that includes the EC2 PublicDNS as its Endpoint URL
- To run the REST proxy within the EC2 client, the Confluent package must first be installed as below:
  ```
  sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
  ```

- Inside the confluent/etc/kafka-rest folder, a kafka-rest.properties file is editted to perform IAM authentication to the MSK cluster:
  ```
  client.security.protocol = SASL_SSL

  # Identifies the SASL mechanism to use.
  client.sasl.mechanism = AWS_MSK_IAM

  # Binds SASL client implementation.
  client.sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="your_access_role_arn";

  # Encapsulates constructing a SigV4 signature based on extracted credentials.
  # The SASL client bound by "sasl.jaas.config" invokes this class.
  client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
  ```

- The REST proxy can then be run inside the EC2 client with the code below:
  ```
  # This code needs to be run inside the confluent/bin folder
  ./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
  ```

- Data is then sent to the API using the altered [user_posting_emulation.py](user_posting_emulation.py) script

### Milestone 6 - Mount the S3 Bucket to Databricks
- The code to mount the S3 bucket to Databricks, the code can be found within the first block of the [pinterest_df_manipulation.ipynb](pinterest_df_manipulation.ipynb) notebook

- Dataframes to contain the data are produced after reading the data into Databricks

### Milestone 7 - Using Spark to Tranform the Data
- A series of tranformations were performed on the data as shown in the [pinterest_df_manipulation.ipynb](pinterest_df_manipulation.ipynb) notebook

### Milestone 8 - Perfrorm Databricks Workloads on AWS MWAA
- Create and upload a DAG file into MWAA environment: [12869112c9e5_dag.py](12869112c9e5_dag.py)
- This was uploaded inside an S3 bucket called "mwaa-dag-bucket"
- Manually trigger the DAG to run a Databricks Notebook

### Milestone 9 - Send Streaming Data to Kinesis and Read this Data Inside Databricks
- The [kinesis_data_streaming.ipynb](kinesis_data_streaming.ipynb) notebook was constructed by creating a Kinesis data stream
- The API was configured to allow Kinesis proxy integration, allow the data to be sent to Kinesis streams
- This allowed the data to be read into Databricks and transformed as seen in the notebook