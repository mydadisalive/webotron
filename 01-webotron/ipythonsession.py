# coding: utf-8
import boto3
from pprint import pprint

client = boto3.client('cloudfront')
paginator = client.get_paginator('list_distributions')
session = boto3.Session(profile_name = 'automation')
s3 = session.resource('s3')
