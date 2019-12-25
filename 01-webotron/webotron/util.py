# -*- coding: utf-8 -*-

"""Region handling."""

from collections import namedtuple
Endpoint = namedtuple('Enpoint', ['name', 'host', 'zone'])

region_to_endpoint = {
    'us-east-2': Endpoint('US East (Ohio)', 's3-website.us-east-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'us-east-1': Endpoint('US East (N. Virginia)', 's3-website.us-east-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'us-west-1': Endpoint('US East (N. California)', 's3-website.us-west-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'us-west-2': Endpoint('US East (Oregon)', 's3-website.us-west-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ca-central-1': Endpoint('Canada (Central)', 's3-website.ca-central-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ap-south-1': Endpoint('Asia Pacific (Mumbai)', 's3-website.ap-south-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ap-northeast-2': Endpoint('Asia Pacific (Seoul)', 's3-website.ap-northeast-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ap-northeast-3': Endpoint('Asia Pacific (Osaka-Local)', 's3-website.ap-northeast-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ap-southeast-1': Endpoint('Asia Pacific (Singapore)', 's3-website.ap-southwest-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ap-southeast-2': Endpoint('Asia Pacific (Sydney)', 's3-website.ap-southwest-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'ap-northeast-1': Endpoint('Asia Pacific (Tokyo)', 's3-website.ap-northeast-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'cn-northwest-1': Endpoint('China (Ohio)', 's3-website.cn-northwest-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'eu-central-1': Endpoint('EU (Frankfurt)', 's3-website.eu-central-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'eu-west-1': Endpoint('EU (Ireland)', 's3-website.us-west-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'eu-west-2': Endpoint('EU (London)', 's3-website.us-west-2.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'eu-west-3': Endpoint('EU (Paris)', 's3-website.eu-west-3.amazonaws.com', 'Z2O1EMRO9K5GLX'),
    'sa-east-1': Endpoint('South America (Sao Paulo)', 's3-website.sa-east-1.amazonaws.com', 'Z2O1EMRO9K5GLX'),
}


def known_region(region):
    """Return true if this is a known region."""
    return region in region_to_endpoint


def get_endpoint(region):
    """Get the s3 website hosting endpoint for this region."""
    return region_to_endpoint[region]