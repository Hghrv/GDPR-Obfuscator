terraform {
  required_providers {
    aws ={
        source = "hashicorp/aws"
        version = "~> 5.100.0"
    }
  }
  backend "s3" {
    bucket = "gdpr-data-storage"
    key= "terraform/state.tfstate"
    region = "eu-west-2"
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