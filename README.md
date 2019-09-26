# Transient EC2 instances with Lambda

This is an example project accompanying a [blog post](https://mraag.xyz/posts/transient-ec2-with-lambda) on using AWS Lambda functions to run transient EC2 instances for periodic jobs. Review the post for details of the motivation behind the application.

## Overview

The project consists of the following components:

- A [Python library](./pie) for calculating the digits of Pi and saving the result to an S3 bucket.
- A [Packer configuration](./image) for building an EC2 image under with the above library and its dependencies.
- An [AWS Lambda function](./lambdas/provision.py) for running an EC2 instance with a specified image
- A [CloudFormation template](./template.yaml) for provision the required infrastructure.

## Usage

Deploying the project to AWS depends on [Packer](https://www.packer.io) and [Python](https://www.python.org).

The Python dependencies are listed under `requirements.txt` and can be installed using `pip`.

```
pip install -r requirements.txt
```

The EC2 image must be built before deploying the CloudFormation stack.

```
make build-image
```

The output will include the AMI ID of the new image, which will look something like the following example.

```
==> Builds finished. The artifacts of successful builds are:
--> amazon-ebs: AMIs were created:
us-east-1: <AMI ID>
```

The Lambda function must be uploaded to a preexisting S3 bucket. You can use any bucket under the
same account or create a new one. An example of how to do that with the AWS CLI is included below.

```
aws s3api create-bucket --acl private --bucket <bucket name> --region us-east-1
```

Set the following environment variables to configure CloudFormation stack deployment.

| Environment Variable | Default Value | Description                             |
| -------------------- | ------------- | --------------------------------------- |
| ARTIFACTS_BUCKET     |               | S3 bucket to store AWS Lambda function. |
| STACK_NAME           |               | Name of the CloudFormation stack.       |
| IMAGE_ID             |               | AWS AMI ID.                             |
| INSTANCE_TYPE        | t2.micro      | The EC2 instance type to run.           |
| DURATION             | 300           | Seconds to run Pi calculation for.      |

Deploy the CloudFormation stack.

```
make deploy
```

The stack will configure a Lambda function, that will run a new EC2 instance with the built image
according to the schedule defined in `template.yaml` (by default every day at 11PM). Alternatively you can test the function by triggering it manually from the [Lambda Management Console](https://console.aws.amazon.com/lambda), the contents of the test event can be arbitrary.

When you've satisfied your curiosity you can delete all the provisioned resources by running the
following command. Ensure you're using the same environment variables, as when you provisioned
the resources.

```
make destroy
```

The S3 buckets you used for storing the Lambda function will not be deleted. If you created a new
bucket, you can delete it manually.

```
aws s3 rm s3://<bucket name> --recursive
aws s3api delete-bucket --bucket <bucket name>
```
