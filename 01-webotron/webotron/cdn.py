# -*- coding: utf-8 -*-

"""Classes for CDN management."""

import uuid
# from pprint import pprint


class DistributionManager:
    """Manage CDN."""

    def __init__(self, session):
        """Create DistributionManager object."""
        self.session = session
        self.client = session.client('cloudfront')

    def find_matching_dist(self, domain_name):
        """Find a matching domain name."""
        distributions = self.client.list_distributions()
        if distributions['DistributionList']['Quantity'] > 0:
            for distribution in distributions['DistributionList']['Items']:
                if distribution['Aliases']['Quantity'] != 0:
                    if domain_name in distribution['Aliases']['Items']:
                        return distribution
        else:
            print("Error - No CloudFront Distributions Detected.")

        return None


    def create_dist(self, domain_name, cert):
        """Create a dist for domain_name using cert."""
        origin_id = 'S3-'+domain_name
        result = self.client.create_distribution(
            DistributionConfig={
                'CallerReference': str(uuid.uuid4()),
                'Aliases': {
                    'Quantity': 1,
                    'Items': [
                        domain_name
                    ]
                },
                'DefaultRootObject': 'index.html',
                'Comment': 'Created by webotron',
                'Enabled': True,
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': origin_id,
                        'DomainName': domain_name+'.s3.amazonaws.com',
                        'S3OriginConfig': {
                            'OriginAccessIdentity': ''
                        }
                    }]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': origin_id,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners': {
                        'Quantity': 0,
                        'Enabled': False,
                    },
                    'ForwardedValues': {
                        'Cookies': {'Forward': 'all'},
                        'Headers': {'Quantity': 0},
                        'QueryString': False,
                        'QueryStringCacheKeys': {'Quantity': 0}
                    },
                    'DefaultTTL': 86400,
                    'MinTTL': 3600,
                },
                'ViewerCertificate': {
                    'ACMCertificateArn': cert['CertificateArn'],
                    'SSLSupportMethod': 'sni-only',
                    'MinimumProtocolVersion': 'TLSv1.1_2016'
                }
            }
        )

        return result['Distribution']

    def await_deploy(self, dist):
        """Wait for dist to be deployed."""
        waiter = self.client.get_waiter('distribution_deployed')
        waiter.wait(Id=dist['Id'], WaiterConfig={
            'Delay': 30,
            'MaxAttempts': 70
        })
