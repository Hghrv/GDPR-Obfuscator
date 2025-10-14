# GDPR-Obfuscator

Obfuscator Project for sensitive data under UK GDPR (General Data Protection Regulation, United Kindom).

This project provides an efficient and secure obfuscating tool that meets current GDPR requirements and that can also be deployed to create resources on a valid AWS account. The tool can easily be integrated in third party applications, for example by setting a streaming event bridge on the AWS console.

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

        Then configure your AWS credentials with the following command:
        aws configure

        A prompt message should appear inviting to enter your AWS credentials. Ensure that the default region name is set to "eu-west-2", and that the default output format is set to  format as below: 

        AWS Access Key ID: ###########
        AWS Secret Access Key: #############
        Default region name: eu-west-2
        Default output format: json

        

      . Terraform 1.13 (Hashicorp installation procedure before terraform backend reconfiguration: optional as already included in requirement.txt)
        pip install python-terraform=1.13.3

      . Make
        pip install make

### AWS Deployment: Follow steps or skip to Make deployment section

      . Step 1 (Use the <-reconfigure> flag after adding terraform backend bloc in main.tf):
        terraform init
        (Without backend s3)

        terraform init -reconfigure
        (With backend S3)

      . Step 2:
        Terraform plan

      . Step 3:
        terraform apply

      or, 
      
### Automated deployement with Make

        Make file

    - Integration
        Uploading a csv file to input s3 bucket will trigger the lambda handler with the file location and the sensitive fields ["name", "email_address"] as lambda events

        - To upload your local csv file to the bucket:
        aws s3 cp /path/to/your/file s3://gdpr-data-storage/new_data/test_file.csv

        Note that the input csv file must be a valid csv with the first row listing the following columns and the second row listing the values.
        Example of valid csv input: "student_id,name,course,cohort,graduation_date,email_address\n1234,'John Smith','Software','December','2024-03-31','j.smith@email.com'"

        - To get the obfuscated result from the output s3:
        aws s3 cp s3://gdpr-obfuscator-ouput/obfuscated_file.csv <you_local_path>

        Alternatively, you may set an envent bridge on the AWS console to set your own events and requests dynamically in order to handle the input and output files (gdpr-data-storage/new_data/test_file.csv and gdpr-obfuscator-ouput/obfuscated_file.csv respectively) in a streaming environment (See link  documentation section to setup EventBridge on your AWS Console)

### Note on Terraform deployment and Passkeys

        Ensure that all package versions are the same across dependencies within the virtual environment.

        . To set your AWS credentials run the folowing sript in your control line interface:

        $ aws configure
        AWS Access Key ID [None]: YOUR_PROVIDED_ACCESS_ID
        AWS Secret Access Key [None]: YOUR_PROVIDED_SECRET_KEY
        Default region name [None]: us-west-2
        Default output format [None]: json

        . Uploading the test csv file into the input s3 bucket:
        aws s3 cp /path/to/your/src/test_file.csv s3://gdpr-data-storage/

        . Downloading the obfuscated csv file locally from the output s3 bucket:
       aws s3 cp s3://gdpr-obfuscator-ouput/obfuscated_file.csv <you_local_path>

### Note on Unit-Testing and Mock-Tests

      In this project, Pytest uses Coverage and Pep8 plugins for PEP8 safety compliance. While the lambda handler was tested with an actual AWS account, the utility modules where tested with mock_aws to simulate s3 buckets and reduce storage costs in the potential event where an event bridge might sent a large quantity of files for tests. This is in order to maintain elasticity of resources. Similarly, separate output and backend s3 buckets are created to avoid reccuring costs (when input and output are processed in the same s3 bucket) according to recommendations on the AWS website.

      Run tests on your terminal with the command below:
      pytest

      Test files in the <test> folder can also be run indidually by specifing the path. For example:
      pytest src/test_lambda_handler.py

      For more detailed printing, add the "-vvvrp" flag as below:
      pytest -vvvrp src/test_lambda_handler.py 

      Running the Makefile altenatively will also securely run the tests by default before deploying the Terraform scripts to create the ressources on the AWS account. Three s3 buckets will be created (input, terraform backend, and output) and the lambda_handler.py will be deployed with all the utility modules and zipped dependencies, which will meet MVP requirements.

      

## Documentation

* More on obfuscation principles
  <https://standards.education.gov.uk/standard/data-anonymisation-pseudonymisation-and-obfuscation#howtommeet>

* Boto3 / Hashicorp
  <https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>

* Moto / AWS Mock Tests
  <https://docs.getmoto.org/en/latest/docs/getting_started.html>

* Terraform documentation
  <https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>

* Amazon Web Services (AWS)
  <https://docs.aws.amazon.com/.html>
  
* AWS_cli
  <https://docs.aws.amazon.com/cli/latest/userguide/cli_s3_code_examples.html>

* EventBridge (on AWS Console)
  <https://docs.aws.amazon.com/.html>

## Licence

Legal Notice:

All commercial rights related to this project are reserved by the owner [TechReturners](https://www.techreturners.com/) (Copyright 2025).
