# GDPR-Obfuscator

Obfuscator Project for sensitive data under UK GDPR (General Data Protection Regulation, United Kindom)

## Context

The present project aims at providing a general-purpose tool to process data being ingested to AWS and intercept personally identifiable information (PII).

Since information stored by Northcoders data projects are intended for bulk data analysis only, there is a requirement under UK GDPR to ensure that all data containing information that could be used to identify an individual should be anonymised.

## The legal framework

Under UK domestic law, the General Data Protection Regulation or UK GDPR is a comprehensive data protection law that came into effect on 25 May 2018, alongside an revised version of the Data Protection Act 2018.

According to [https://www.gov.uk/data-protection](https://www.gov.uk/data-protection), data protection in the UK is mainly governed by the UK GDPR and the Data Protection Act of 2018. UK data protection principles specifically restricts how personal information is used by organizations in order to ensure data protection and privacy for individuals (data subjects).

These ‘data protection principles’ are strict rules requiring that people or entities responsible for using personal data must ensure (unless an exemption applies) the following legal requirements are met:

    - Fair, lawful and transparent use of data

    - Use of information for specific purposes

    - Adequate and relevant use of information limited to only necessary data

    - Accuracy and update of information

    - Data Storage no longer than is necessary

    - Appropriate data integrity and security, including protection against unlawful or unauthorised processing, access, loss, destruction or damage

In addition to those legal requirements, there is also a strong emphasis on the processing of more sensitive data (Ex: race, ethnicity, religion, biometric id, health, background checks etc.) as data subjects carry fundamental rights such as the right to transparency and access to information, right to rectification/erasure, objections and also restrictions on automated decision-making. Therefore personal data must also be handled in accordance with these principles.

## A Descriptive Overview of the Project

### Objectives

The GDPR framework described previously actually constitutes the rationale for building and Obfuscator to secure sensitive data. In this project we will precisely follow those personal data guidelines as stated in the UK legislation at: <https://www.legislation.gov.uk/eur/2016/679/contents>

(The Principles relating to processing of personal data, Article 5 to Article 11A).

Building our Data Obfuscator library under GDRP regulation and guidelines ensures that data processing platforms and developers can have a viable and optimal option at hand providing up-to-date and secured solutions.

### MVP (Most Valuable Product)

Building a fully tested and automated GDPR Obfuscator for deployment on AWS and third-party software integration, in other words an obfuscation tool that can be integrated as a library module into a Python codebase.

The tool is to be supplied with the S3 location of a file containing sensitive information, and the names of the affected fields. It should create a new file or byte stream object containing an exact copy of the input file but with the sensitive data replaced with obfuscated strings. The calling procedure will handle saving the output to its destination. It is expected that the tool will be deployed within the AWS account.

### Framework and Purpose

      Linux CLI

      Python 3

      Terraform for AWS resources creation

      Pytest for testing

      Boto3 for aws s3_client handling

      Moto  for mock-testing / secret-manager

      Make for automated deployment of project

## How to use

    - System Requirements
      . Linux cli or WSL for Windows
      . Python 3.12.7
      . Terraform 1.13
      . AWS_cli 1.42.40
      . Make
 
    - Installation
      . Clone repository
        git clone <link_to_git_repository>
      . Create and activate virtual environment and export pythonpath
        python -m venv venv
        source venv/bin/activate
        export PYTHONPATH=$pwd

      . Install requirements
        pip install tequirements.txt

      . AWS_cli 1.42.40
        python -m pip install awscli=1.42.40

      . Terraform 1.13 (Hashicorp installation procedure before terraform backend reconfiguration: optional as already included in requirement.txt)
        pip install python-terraform=1.13.3

      . Make
        pip install make

    - AWS Deployment: Follow steps or skip to Make deployment
      . Step 1 (Use the <-reconfigure> flag after adding terraform backend bloc in main.tf): 
        terraform init -reconfigure

      . Step 2:
        Terraform plan

      . Step 3:
        terraform apply

      or, 
      
      Automated deployement with Make
        Make file

    - Integration
        Uploading a csv file to input s3 bucket will trigger the lambda handler with the file location and the sensitive fields ["name", "email_address"] as lambda events.


    - Note on Terraform deployment and Passkeys:
        Ensure that all package versions are the same across dependencies within the virtual environment.

        . To set your AWS credentials run the folowing sript in your control line interface:

        $ aws configure
        AWS Access Key ID [None]: YOUR_PROVIDED_ACCESS_ID
        AWS Secret Access Key [None]: YOUR_PROVIDED_SECRET_KEY
        Default region name [None]: us-west-2
        Default output format [None]: json

        . Uploading the test csv file into the input s3 bucket:
        aws s3 cp /path/to/your/src/test_file.csv s3://gdpr-data-storage/




    - Note on Unit-Testing and Mock-Tests

## Documentation

* More on obfuscation principles
  <https://standards.education.gov.uk/standard/data-anonymisation-pseudonymisation-and-obfuscation#howtommeet>

* Boto3 / Hashicorp
  <https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>

* Moto

* Terraform documentation
  <https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>

* Amazon Web Services (AWS)
  
* AWS_cli
  <https://docs.aws.amazon.com/cli/latest/userguide/cli_s3_code_examples.html>

## Legal Notice

All commercial rights related to this project are reserved by the owner [Tech Returners](https://www.techreturners.com/) (Copyright 2025).
