# ACM Cert Validation

Lambda to back a custom resource which grabs the dns configuration required to validate ACM Certs.

Made with ❤️ by Trek10. Available on the [AWS Serverless Application Repository](https://aws.amazon.com/serverless)

## Usage

```yml
Parameters:
  DomainName:
    Type: String

Resources:
  ACMCertValidation:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: arn:aws:serverlessrepo:us-east-1:498899591819:applications/acm-cert-validation
        SemanticVersion: 0.0.0

  DNSConfiguration:
    Type: Custom::DNSConfiguration
    Condition: IsPrimary
    Properties:
      ServiceToken: !GetAtt ACMCertValidation.Outputs.LambdaArn
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
