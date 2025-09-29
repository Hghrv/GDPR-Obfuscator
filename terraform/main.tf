terraform {
  required_providers {
    aws ={
        source = "hashicorp/aws"
        version = "~> 5.100.0"
    }
  }

  backend "s3" {
    bucket         = "gdpr-terraform-state-bucket" # Replace with your bucket name
    key            = "terraform/.terraform/terraform.tfstate" # Define the path for the state file
    region         = "eu-west-2"                # Match your bucket's region
    encrypt        = true
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
        ProjectName = "GDPR Obfuscator"
        Team = "tech-returners"
        DeployedFrom = "Terraform"
        Repository= "gdpr-project"
        Enviroment= "dev"
    }
  }
}