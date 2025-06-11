This folder contains **AWS IAM Role and Policy definitions** required for the ETL pipeline infrastructure. These policies implement the **least privilege** principle, granting only necessary permissions to each service.

---

## Contents

* **lambda\_execution\_role\_policy.json**
  IAM policy for Lambda functions to access S3 buckets (raw & clean) and CloudWatch Logs.

* **glue\_execution\_role\_policy.json**
  IAM policy for Glue jobs and crawlers with restricted S3 and Glue Data Catalog access.

* **glue\_crawler\_role\_policy.json**
  Inline policy attached to the Glue Crawler role for reading from S3 and catalog actions.

* **redshift\_spectrum\_access\_policy.json**
  IAM policy granting Redshift Spectrum permissions to access Glue Catalog and S3 clean data.

* **pass\_role\_policy.json**
  Allows services to assume or pass roles where necessary, with explicit resource ARNs.

---

## Usage

1. **Attach** these policies to their respective IAM roles in your AWS environment.
2. **Modify** bucket names and ARNs as necessary before deploying to your environment.
3. **Do not expose** sensitive ARNs or account numbers if sharing publicly.

---

## Security & Best Practices

* These policies follow **least privilege** principles.
* **Review and customize** permissions based on your environment and compliance requirements.
* Avoid using wildcard `"*"` in resource ARNs unless absolutely necessary.
* Use **IAM role names and policy names** consistently for clarity and maintainability.

---

## Notes

* Bucket names in policies are placeholders. Replace `"lana-etl-pipeline"` with your actual bucket names.
* The `PassRole` policy allows Glue jobs to pass execution roles — critical for Glue job execution.
* AWS managed policies like `AWSLambdaBasicExecutionRole` and `AWSGlueServiceRole` are used alongside these custom policies for base permissions.
