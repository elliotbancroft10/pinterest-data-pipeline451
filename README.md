### Pinterest Data Pipeline

## Contents

## About the project
This project retrieves pinterest, user and geographical data from an RDS dataset. The data is then stored in a DataBricks mounted S3 bucket.

To transfer the data into the S3 bucket, an API was created using AWS API Gateway, which in turn allows the data to be sent via the MSK cluster, to the connected S3 bucket using the IAM MSK authentication package.

## Installation
 - You will need to sign in to the AWS console as an IAM user
 - Create and store a .pem key pair file relating to your EC2 instance and store it in a local directory that will be used to configure your EC2 Kafka Client
 - Connect to the SSH client
 - Install Kafka in your EC2 client ensuring the version is compatible with the version your MSK cluster is running on
 - If your cluster needs IAM authentication, install the IAM MSK authentication package in your client
 - Make sure you have the necessary permissions to access the MSK cluster, you may need an IAM role for this
 - Create your Kafka topics within your EC2 client 


## Usage

## File Structure

## Licence Information
