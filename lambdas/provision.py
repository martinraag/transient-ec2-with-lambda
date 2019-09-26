import json
import logging
import os
import time

import boto3

BUCKET = os.environ.get("BUCKET")
DURATION = os.environ.get("DURATION")
IMAGE_ID = os.environ.get("IMAGE_ID")
INSTANCE_PROFILE = os.environ.get("INSTANCE_PROFILE")
INSTANCE_TYPE = os.environ.get("INSTANCE_TYPE")
# fmt: off
USER_DATA = (
    "#!/bin/bash\n"
    f"pie {DURATION} {BUCKET}\n"
    "shutdown -h now"
)
# fmt: on

ec2 = boto3.client("ec2")
log = logging.getLogger("provision")


def run_instance(image_id, user_data, instance_type, instance_profile):
    """Run EC2 instance in given region."""

    log.info(
        f"Run instance image={image_id} type={instance_type} profile={instance_profile}"
    )
    res = ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        InstanceInitiatedShutdownBehavior="terminate",
        IamInstanceProfile={"Arn": instance_profile},
        UserData=user_data,
    )
    instance_id = res["Instances"][0]["InstanceId"]
    log.info(f"Run instance success id={instance_id}")
    return instance_id


def handler(event, context):
    run_instance(IMAGE_ID, USER_DATA, INSTANCE_TYPE, INSTANCE_PROFILE)
