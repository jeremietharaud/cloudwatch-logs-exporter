# Simple AWS Cloudwatch Logs exporter

A Prometheus Cloudwatch Logs exporter written in Python.

## Metrics

| Metrics  | Dimensions | Labels | Description |
| ------  | ------ | ------ | ----------- |
| aws\_logs\_stored_bytes | log_group | log_group | Total space in bytes used by the log group |

## Configuration

Credentials to AWS are provided in the following order:

- Environment variables (AWS\_ACCESS\_KEY\_ID and AWS\_SECRET\_ACCESS\_KEY)
- Shared credentials file (~/.aws/credentials)
- IAM role for Amazon EC2

For more information see the [AWS Python SDK Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)

### AWS IAM permissions

The exporter needs read access to Cloudwatch Logs service for describing log streams:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "*"
        }
    ]
}
```
