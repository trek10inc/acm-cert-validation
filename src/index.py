import boto3
import json
import time
from crhelper import CfnResource
import logging

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=True, log_level='DEBUG', boto_level='CRITICAL')


def get_dns_configuration(domain_name):
    acm = boto3.client('acm')
    while True:
        response = acm.list_certificates(
            CertificateStatuses=['PENDING_VALIDATION']
        )
        print('Checking for certificate:', json.dumps(response, default=str))
        for cert in response['CertificateSummaryList']:
            if cert['DomainName'] == domain_name:
                print('Found the certificate!')
                res = acm.describe_certificate(CertificateArn=cert['CertificateArn'])
                print(f'Certificate: {json.dumps(res, default=str)}')
                validation_methods = res['Certificate']['DomainValidationOptions']
                for validation_method in validation_methods:
                    if 'ResourceRecord' in validation_method:
                        return res['Certificate']['DomainValidationOptions'][0]['ResourceRecord']
        time.sleep(5)


@helper.create
def create(event, context):
    logger.info('Got Create')
    domain_name = event.get('ResourceProperties', {}).get('DomainName')
    if not domain_name:
        raise Exception('DomainName must be provided')

    dns_configuration = get_dns_configuration(domain_name)
    logger.info(f'DNS Configuration: {json.dumps(dns_configuration, default=str)}')
    helper.Data.update(dns_configuration)

    return domain_name


@helper.delete
@helper.update
def no_op(_, __):
    pass


def handler(event, context):
    helper(event, context)
