# -*- coding: utf-8 -*-

"""Classes for S3 buckets."""

from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError
import util


class BucketManager:
    """Manage an S3 bucket."""

    def __init__(self, SESSION):
        """Create a BucketManager object."""
        self.session = SESSION
        self.s3 = self.session.resource('s3')

    def get_region_name(self, bucket):
        """Get the bucket's region name."""
        client = self.s3.meta.client
        bucket_location = client.get_bucket_location(Bucket=bucket.name)
        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Get the bucket URL for this bucket."""
        return "http://"+bucket.name+"."+util.get_endpoint(self.get_region_name(bucket)).host

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator for all objects in bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create a new bucket with name bucket_name, or return existing one."""
        s3_bucket = None
        # try:
        s3_bucket = self.s3.create_bucket(
            Bucket=bucket_name,
        )
        return s3_bucket

    def set_policy(self, bucket):
        """Set a bucket policy to be read by everyone for bucket."""
        policy = """
        {
            "Version": "2012-10-17",
            "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::%s/*"]
            }]
        }
        """ % bucket.name
        policy = policy.strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        """Configure website."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    @staticmethod
    def upload_file(bucket, path, key):
        """Upload path to s3_bucket at key."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type,
            }
        )

    def sync(self, pathname, bucket_name):
        """Sync bucket."""
        bucket = self.s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for path in target.iterdir():
                if path.is_dir():
                    handle_directory(path)
                if path.is_file():
                    self.upload_file(bucket, str(path), str(path.relative_to(root)))

        handle_directory(root)
