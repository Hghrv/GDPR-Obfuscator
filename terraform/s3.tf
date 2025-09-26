resource "aws_s3_bucket" "gdpr-data" {
    bucket = "gdpr-data-storage"
    tags = {
        Name = "gdpr bucket"
    }
    force_destroy = true
}