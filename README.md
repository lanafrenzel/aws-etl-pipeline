# Serverless ETL Pipeline: Ingest API Data to Redshift via S3 and Glue

## Project Overview

This project demonstrates building a **serverless, automated ETL pipeline** on AWS that ingests data from a public API, transforms it with AWS Glue, and loads it into Amazon Redshift Serverless for analysis. It uses AWS managed services and aims to stay within the AWS Free Tier.

---

## Goals

* Master AWS Data Engineering tools: Glue, S3, Lambda, Redshift, IAM, CloudWatch, Step Functions
* Build a production-ready ETL pipeline with error handling, retries, and testing
* Create CI/CD-friendly code and infrastructure
* Follow best practices for security and maintainability

---

## Architecture

```
[External API]
     |
  [Lambda: Extract]  ←──── Scheduler (EventBridge)
     |
  [S3 Raw Bucket] ───→ [AWS Glue Job: Transform]
     |
  [S3 Clean Bucket]
     |
  [AWS Glue Crawler] → [Amazon Redshift Serverless]
                      ← Query via SQL or BI tools
```

---

## AWS Services Used

* Orchestration: AWS Step Functions + EventBridge
* Compute: AWS Lambda (Python)
* Storage: Amazon S3 (Raw & Clean buckets)
* Data Transformation: AWS Glue (PySpark)
* Data Warehouse: Amazon Redshift Serverless (Free Tier)
* Monitoring: CloudWatch + Alarms
* Security: IAM Roles & Policies (Least Privilege)
* Testing: Pytest + moto + Glue local testing
* CI/CD: AWS CodePipeline or GitHub Actions

---

## Features

* Fully automated daily ETL pipeline triggered by EventBridge scheduler
* Retry logic and error handling on API extraction
* Data validation and schema evolution support in Glue transformations
* YAML configuration for pipeline flexibility
* Secure IAM policies following least privilege principle
* Unit and integration tests for Lambda and Glue jobs
* CI/CD ready with clean, modular code structure

---

## Data Sources

Public APIs used:

* MarketStack API ([https://marketstack.com/](https://marketstack.com/))

---

## Repository Structure

```
/aws-serverless-etl/
├── lambda/
│   └── extract_api_data.py          # Lambda function for API data extraction
├── glue_jobs/
│   └── transform_data.py            # Glue job for data transformation
├── infrastructure/
│   ├── cloudformation.yml           # Infrastructure as Code (CloudFormation/CDK)
│   └── iam_policies/                # IAM policies with least privilege
├── config/
│   └── pipeline_config.yml          # Pipeline configuration file
├── README.md                        # This file
└── LICENSE                          # License file
``` 

---

## Technologies & Libraries

* Python 3.x
* AWS SDK (boto3)
* PySpark (Glue transformations)
* Pytest and moto (testing)
* AWS CLI / CloudFormation / CDK
* YAML (configuration)

---

## References

* AWS Glue Documentation: [https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
* Amazon Redshift Serverless: [https://aws.amazon.com/redshift/serverless/](https://aws.amazon.com/redshift/serverless/)
* AWS Lambda Guide: [https://docs.aws.amazon.com/lambda/latest/dg/welcome.html](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* AWS Step Functions: [https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
* boto3 AWS SDK: [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

## Contributions & Issues

Contributions welcome! Please open issues or pull requests.

---

## License

MIT License — see LICENSE file.

---

## Acknowledgments

Thanks to the AWS community and open-source tools enabling scalable ETL pipelines.

---

Happy Data Engineering! 🚀
— Lana Frenzel
