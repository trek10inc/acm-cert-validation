# ACM Cert Validation

Lambda to back a custom resource which grabs the dns configuration required to validate ACM Certs.

Made with ❤️ by Trek10. Available on the [AWS Serverless Application Repository](https://aws.amazon.com/serverless)

## Usage

For each region this is deployed under, you'll see an SSM parameter was created that contains the ARN of the lambda function you must use as the custom resource's `ServiceToken`

```yml
Parameters:
  ValidationFunctionArn:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /sar/acm-cert-validation/lambda-arn
  DomainName:
    Type: String

Resources:
  DNSConfiguration:
    Type: Custom::DNSConfiguration
    Properties:
      ServiceToken: !Ref ValidationFunctionArn
      DomainName: !Ref DomainName

  SSLCertificate:
    Type: AWS::CertificateManager::Certificate
    Properties:
      DomainName: !Ref DomainName
      SubjectAlternativeNames:
        - !Sub '*.${DomainName}'
      ValidationMethod: DNS

  RecordSet:
    Type: AWS::Route53::RecordSet
    Properties:
      Comment: For DNS Validation
      HostedZoneName: !Sub ${DomainName}.
      Name: !GetAtt DNSConfiguration.Name
      Type: !GetAtt DNSConfiguration.Type
      ResourceRecords:
        - !GetAtt DNSConfiguration.Value
      TTL: '0'
```

## License

MIT No Attribution (undefined)
