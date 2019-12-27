# -*- coding: utf-8 -*-

"""Classes for Certificate Management in AWS."""


class CertificateManager:
    """Manage an ACM certificate."""

    def __init__(self, session):
        """Create CertificateManager object."""
        self.session = session
        self.client = session.client('acm', region_name='us-east-1')

    def cert_matches(self, cert_arn, domain_name):
        """Find certificate."""
        cert_details = self.client.describe_certificate(CertificateArn=cert_arn)
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                return True
            if name[0] == '*' and domain_name.endswith(name[1:]):
                return True
        return False

    def find_matching_cert(self, domain_name):
        """Find a certificate matching domain_name."""
        paginator = self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.cert_matches(cert['CertificateArn'], domain_name):
                    return cert
        return None
