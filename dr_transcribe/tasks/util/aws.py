import json

import boto3
from botocore import UNSIGNED
from botocore.config import Config


class S3Helper:
    def __init__(self, region_name, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            region_name=region_name,
            config=Config(signature_version=UNSIGNED),
        )

    def read_json(self, file_key):
        s3_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
        file_content = s3_response["Body"].read().decode("utf-8")
        json_data = json.loads(file_content)
        return json_data

    def read_file(self, file_path):
        s3_response = self.s3_client.download_file(
            self.bucket_name,
            self.key,
            file_path,
        )
        return s3_response
