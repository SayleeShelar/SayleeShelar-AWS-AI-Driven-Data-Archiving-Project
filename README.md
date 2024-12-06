
---

# AWS AI-Driven Data Archiving Project

## Overview

This project implements an AI-enhanced data archiving solution using **AWS Serverless** technologies, including **AWS Lambda**, **Amazon SageMaker**, and **Amazon S3**. The goal is to automate file archival based on file metadata, such as last modified date and size, optimizing storage costs by moving infrequently accessed files to **S3 Glacier**. 

The implementation has two main stages:
1. **Before SageMaker Integration**: A rule-based Lambda function archives files older than a specified threshold (e.g., 30 days).
2. **After SageMaker Integration**: An AI model deployed on SageMaker predicts file archival needs, making the process smarter and more adaptable.

---

## Why Use AI?

A simple rule-based approach (archiving files older than a threshold) is efficient for predictable data patterns. However, this method has limitations:
- **Complex Patterns**: Not all files are used uniformly. Some files, despite being old, might be frequently accessed, while others may remain unused shortly after creation.
- **Scalability**: With large datasets, static rules may result in inefficiencies, such as archiving important files or retaining unused files.
- **Flexibility**: AI allows the system to adapt dynamically based on metadata, such as file size, last modified date, and access frequency, reducing manual oversight.

By leveraging AI, this project improves the decision-making process, ensuring that archival decisions are more precise and tailored to real-world file usage patterns.

---

## Features

- **Automated File Archival**: Moves files to S3 Glacier based on metadata and AI predictions.
- **Scalable and Serverless**: Uses AWS Lambda and SageMaker for scalability without server management.
- **Cost Optimization**: Reduces storage costs by archiving infrequently accessed files.
- **Real-Time Processing**: Automatically processes files uploaded to S3.

---

## Project Structure

```
AWS-Data-Archiving-Project/
├── data/                       # Dataset for testing and training
│   └── metadata.csv            # Metadata of files
├── lambda/                     # Lambda function code
│   ├── lambda_original.py      # Lambda function before SageMaker integration
│   ├── lambda_with_sagemaker.py # Lambda function after SageMaker integration
├── model/                      # Model scripts
│   ├── model_training.py       # Code to train and evaluate the model
│   ├── inference.py            # Script for SageMaker inference
├── s3_upload/                  # S3-related scripts
│   └── upload_to_s3.py         # Script to upload files to S3
├── notebooks/                  # Jupyter notebook for SageMaker
│   └── sagemaker_notebook.ipynb # Notebook for training and deployment
├── docs/                       # Documentation
│   └── project_report.pdf      # Detailed project report
├── README.md                   # This file
├── .gitignore                  # Files and directories to ignore
```

---

## Prerequisites

Before starting, ensure the following:
- **AWS Account**: Set up and configure the AWS CLI (`aws configure`).
- **Python 3.x**: Installed on your system.
- Required Python libraries:
  ```bash
  pip install boto3 sagemaker scikit-learn joblib
  ```

---

## Implementation Steps

### 1. Create an S3 Bucket
1. Log in to the AWS Management Console.
2. Navigate to S3 and create a bucket (e.g., `saylee-s3-archive-bucket`).
3. Enable event notifications in the bucket to trigger Lambda functions when files are uploaded.

### 2. Deploy the Lambda Function (Before SageMaker Integration)
1. Navigate to the Lambda service in AWS.
2. Create a new function and upload `lambda_original.py` from the `lambda/` folder.
3. Assign an IAM role with permissions for S3 operations.
4. Test the function by uploading files to the S3 bucket to verify that files older than 30 days are archived to Glacier.

### 3. Train and Deploy the Model on SageMaker
1. Use the `model_training.py` script or `sagemaker_notebook.ipynb` to:
   - Train the logistic regression model using the dataset (`metadata.csv`).
   - Package the trained model and `inference.py` into `model.tar.gz`.
   - Upload the tarball to S3 and deploy it as a SageMaker endpoint.
   
2. Note the SageMaker endpoint name for integration with the Lambda function.

### 4. Deploy the Lambda Function (After SageMaker Integration)
1. Replace the existing Lambda function code with `lambda_with_sagemaker.py`.
2. Update the Lambda function with the SageMaker endpoint name.
3. Assign an IAM role with permissions for both S3 and SageMaker.
4. Test the updated Lambda function to ensure that files are processed using SageMaker predictions.

### 5. Test the Complete System
- Upload test files to your S3 bucket.
- Verify:
  - **Before SageMaker Integration**: Files older than 30 days are archived to Glacier.
  - **After SageMaker Integration**: Lambda invokes SageMaker to predict if a file should be archived, and archives the file accordingly.

### 6. Monitor and Optimize
- Use Amazon CloudWatch to monitor Lambda execution and SageMaker endpoint usage.
- Retrain the model periodically with updated metadata for improved accuracy.

---

## Usage

### Uploading Files
1. Upload files to the S3 bucket (`saylee-s3-archive-bucket`).
2. Ensure files have metadata, such as last modified date and size.

### File Archival Process
- **Rule-Based (Before SageMaker)**: Lambda archives files older than the threshold (e.g., 30 days).
- **AI-Driven (After SageMaker)**: Lambda invokes SageMaker, which predicts whether files should be archived.

---

## Example Workflow

1. A file (`example.txt`) is uploaded to the S3 bucket.
2. The Lambda function triggers and processes the file's metadata.
3. **Before SageMaker**:
   - If the file is older than 30 days, it is archived to S3 Glacier.
4. **After SageMaker**:
   - Lambda invokes the SageMaker endpoint to predict archival needs.
   - If the model predicts "archive," the file is moved to S3 Glacier.

---

## Key Notes

- **Why AI?**: While rule-based systems work for simple scenarios, AI adds flexibility and intelligence by adapting to complex data patterns. This reduces unnecessary archiving of important files and ensures better utilization of storage resources.
- **Serverless Scalability**: AWS services ensure seamless scaling as data volume grows.
- **Cost Savings**: Automates the move of infrequently accessed files to S3 Glacier, reducing storage expenses.

---

