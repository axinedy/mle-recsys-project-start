#!/bin/sh

./mounts3.sh
cp s3-bucket/recommendations.parquet .
cp s3-bucket/similar.parquet .
cp s3-bucket/top_popular.parquet .
umount s3-bucket

