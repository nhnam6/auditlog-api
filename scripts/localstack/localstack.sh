#!/bin/bash

# sqs
awslocal sqs create-queue --queue-name log-queue
awslocal sqs create-queue --queue-name export-queue

# s3
awslocal s3 mb s3://logs-export
