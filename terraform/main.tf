provider "aws" {
  region = var.AWS_REGION
  access_key = var.AWS_KEY
  secret_key = var.AWS_SECRET
}

resource "aws_s3_bucket" "food-truck-bucket" {
    bucket = "c21-kieran-food-truck"
    
    tags = {
        Name = "C21 Kieran Food Truck Bucket"
        Environment = "Dev"
    }
}

resource "aws_glue_catalog_database" "food-truck-database" {
  name = "c21-kieran-food-truck-db"
}

resource "aws_iam_role" "food-truck-role" {
  name = "AWSGlueServiceRole-c21-kieran-food-truck-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue-service-policy" {
  role       = aws_iam_role.food-truck-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "s3-access" {
  name = "c21-kieran-food-truck-s3-access"
  role = aws_iam_role.food-truck-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.food-truck-bucket.arn}/*"
      }
    ]
  })
}

resource "aws_glue_crawler" "food-truck-crawler" {
  database_name = aws_glue_catalog_database.food-truck-database.name
  name          = "c21-kieran-food-truck-crawler"
  role          = aws_iam_role.food-truck-role.arn

   s3_target {
    path           = "s3://${aws_s3_bucket.food-truck-bucket.id}/input/"
    exclusions     = ["s3://${aws_s3_bucket.food-truck-bucket.id}/output/"]
  }
}