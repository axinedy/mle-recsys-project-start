#!/bin/sh
export $(cat .env | xargs)
echo "$S3_ACCESS_KEY:$S3_SECRET_KEY" > .passwd-s3fs
s3fs s3-student-mle-20240325-3ac233b55a s3-bucket -o passwd_file=.passwd-s3fs -o url=https://storage.yandexcloud.net
