#!/usr/bin/env python3
from dotenv import load_dotenv
import boto3
import os
 
load_dotenv()
session = boto3.session.Session()
s3 = boto3.client(
    service_name = 's3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
 
bucket_name = os.getenv("S3_BUCKET_NAME")
files = []
sizes = []
 
 
if s3.list_objects(Bucket=bucket_name).get('Contents'):
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        cur_key = key['Key']
        response = s3.head_object(Bucket = bucket_name, Key = cur_key)
        cur_size = response['ContentLength']
        print(f"file {cur_key} weights {cur_size} bytes")
        files.append(cur_key)
        sizes.append(cur_size)
 
total_weight = sum(sizes)
print(f"Total weight of all files in bucket = {total_weight}")