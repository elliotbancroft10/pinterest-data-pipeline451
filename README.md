### Pinterest Data Pipeline
# An AICore Data Engineering Project

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
  <details>
    <summary><strong>Click to expand</strong></summary>
    <p style="background-color: #FFAF82; padding: 10px;">
      This is the subtext with a small grey banner.
    </p>
  </details>

* [Apache Spark](https://spark.apache.org/docs/latest/)
  <details>
    <summary><strong>Click to expand</strong></summary>
    <p style="background-color: #FFAF82; padding: 10px;">
      This is the subtext with a small grey banner.
    </p>
  </details>

# AWS Resources
* The [requests](https://docs.python-requests.org/en/latest/) package is commonly used for making HTTP requests in Python.

## Data <a name="data"></a>

## Setup and Usage <a name="setup_and_usage"></a>

## File Structure <a name="file_structure"></a>
