## Amazon CloudFront Detailed Guide

### Introduction to Amazon CloudFront

Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds. It integrates with other AWS services to provide an easy-to-use and cost-effective way to distribute content.

### Key Features of Amazon CloudFront

- **Global Distribution**: CloudFront has a global network of edge locations to ensure low latency and high performance.
- **Security**: CloudFront integrates with AWS Shield, AWS WAF, and AWS Certificate Manager to provide robust security for your applications.
- **Programmability**: Lambda@Edge allows you to run code closer to users of your application, enabling real-time customization.
- **Cost-Effective**: Pay-as-you-go pricing model helps to control costs.
- **Seamless Integration**: Works seamlessly with other AWS services like S3, EC2, and Route 53.

### Setting Up Amazon CloudFront

#### Step 1: Creating a CloudFront Distribution

1. **Login to AWS Management Console**: Navigate to the CloudFront service.
2. **Create Distribution**:
   - Select the type of distribution: `Web` or `RTMP`. For this guide, we'll focus on `Web`.
   - Click on "Create Distribution" under the Web section.

#### Step 2: Configuring the Distribution

1. **Origin Settings**:
   - **Origin Domain Name**: The domain name of the origin (e.g., your S3 bucket or web server).
   - **Origin Path**: Optional path to append to the origin domain name.
   - **Origin ID**: A unique identifier for the origin.

2. **Default Cache Behavior Settings**:
   - **Viewer Protocol Policy**: Choose between HTTP and HTTPS.
   - **Allowed HTTP Methods**: Select the HTTP methods (GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE).
   - **Cache Based on Selected Request Headers**: Choose how CloudFront caches content based on request headers.

3. **Distribution Settings**:
   - **Price Class**: Select the regions where you want CloudFront to distribute your content.
   - **AWS WAF Web ACL**: Attach a Web ACL to the distribution for additional security.
   - **Alternate Domain Names (CNAMEs)**: Add custom domain names if necessary.
   - **SSL Certificate**: Choose between default CloudFront SSL certificate or a custom certificate.

4. **Create Distribution**: Review the settings and click on "Create Distribution".

#### Step 3: Configuring Your Origin

- **Amazon S3**: Ensure your bucket policies allow CloudFront to access the content.
- **Custom Origin (e.g., EC2)**: Ensure your server is configured to handle requests from CloudFront.

#### Step 4: Testing Your Distribution

- Once the distribution status changes to "Deployed", test it by accessing the CloudFront domain name in a web browser.
- Verify that the content is served correctly and check the headers to ensure caching is working as expected.

### Advanced Configuration

#### Caching Strategies

- **Cache Invalidation**: Use invalidation requests to remove objects from CloudFront edge caches before they expire.
- **TTL Settings**: Configure Time-to-Live (TTL) settings to control how long objects are cached.

#### Security

- **HTTPS**: Enforce HTTPS to ensure data is encrypted in transit.
- **Access Control**: Use signed URLs and signed cookies to restrict access to content.
- **AWS WAF**: Configure rules in AWS WAF to protect against common web exploits.

#### Monitoring and Logging

- **CloudFront Access Logs**: Enable logging to capture detailed information about every user request.
- **AWS CloudWatch**: Use CloudWatch metrics to monitor CloudFront performance and set up alarms for specific events.

### Real-World Example: E-Commerce Site

#### Scenario

An e-commerce company wants to use CloudFront to distribute its website content globally, ensuring high availability, security, and scalability.

#### Steps

1. **Create an S3 Bucket for Static Content**: Store images, CSS, and JavaScript files.
2. **Set Up CloudFront Distribution**:
   - Origin: S3 bucket and web servers.
   - Viewer Protocol Policy: Redirect HTTP to HTTPS.
   - Enable Caching and Configure TTL.
3. **Configure SSL**: Use AWS Certificate Manager (ACM) to create a custom SSL certificate.
4. **Security**:
   - Enable AWS WAF to protect against SQL injection and XSS.
   - Use signed URLs for sensitive content.
5. **Monitoring**: Set up CloudWatch alarms for metrics like 4xx and 5xx errors.

#### Terraform Script Example

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-ecommerce-content"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_cloudfront_distribution" "my_distribution" {
  origin {
    domain_name = aws_s3_bucket.my_bucket.bucket_regional_domain_name
    origin_id   = "myS3Origin"
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    target_origin_id       = "myS3Origin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

### Conclusion

Amazon CloudFront is a powerful and flexible CDN service that can significantly improve the performance, security, and scalability of your web applications. By following this guide, you can set up and configure CloudFront to meet the specific needs of your business.

### Further Reading

- [Amazon CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [Best Practices for Amazon CloudFront](https://aws.amazon.com/cloudfront/getting-started/best-practices/)
- [AWS Whitepapers and Guides](https://aws.amazon.com/whitepapers/)

### Real-World Examples of Amazon CloudFront

#### Example 1: E-Commerce Website

**Scenario**: An e-commerce company wants to use CloudFront to deliver its website content globally, ensuring high availability, security, and scalability. The company has static content (images, CSS, JavaScript) stored in an S3 bucket and dynamic content served by an EC2 instance.

**Steps**:

1. **Create an S3 Bucket for Static Content**:
   - Store images, CSS, and JavaScript files in an S3 bucket.
   - Ensure the bucket policy allows CloudFront to access the content.

2. **Set Up CloudFront Distribution**:
   - **Origin**: S3 bucket for static content and EC2 instance for dynamic content.
   - **Viewer Protocol Policy**: Redirect HTTP to HTTPS to ensure secure connections.
   - **Cache Behavior**: Configure caching settings to optimize performance.
   - **SSL Configuration**: Use AWS Certificate Manager (ACM) to create a custom SSL certificate for the domain.
   - **Security**: Enable AWS WAF to protect against common web exploits like SQL injection and cross-site scripting (XSS).
   - **Access Control**: Use signed URLs for sensitive content (e.g., user account pages).

3. **Monitoring and Logging**:
   - Enable CloudFront access logs to capture detailed information about user requests.
   - Use AWS CloudWatch to monitor performance metrics and set up alarms for error rates (e.g., 4xx and 5xx errors).

**Terraform Script**:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-ecommerce-content"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_cloudfront_distribution" "my_distribution" {
  origin {
    domain_name = aws_s3_bucket.my_bucket.bucket_regional_domain_name
    origin_id   = "myS3Origin"
  }

  origin {
    domain_name = "my-ec2-instance.example.com"
    origin_id   = "myEC2Origin"
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    target_origin_id       = "myS3Origin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  cache_behavior {
    path_pattern           = "/dynamic/*"
    target_origin_id       = "myEC2Origin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }

    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = "arn:aws:acm:us-east-1:123456789012:certificate/your-certificate-id"
    ssl_support_method             = "sni-only"
  }
}
```

#### Example 2: Streaming Media Platform

**Scenario**: A streaming media platform wants to deliver video content to users globally with low latency and high quality. The platform uses an S3 bucket to store video files and wants to use CloudFront for content delivery.

**Steps**:

1. **Create an S3 Bucket for Video Content**:
   - Store video files in an S3 bucket.
   - Set appropriate bucket policies to allow CloudFront access.

2. **Set Up CloudFront Distribution**:
   - **Origin**: S3 bucket for video files.
   - **Viewer Protocol Policy**: Redirect HTTP to HTTPS.
   - **Cache Behavior**: Optimize caching settings for video content (e.g., longer TTL for static video files).
   - **SSL Configuration**: Use ACM to create a custom SSL certificate.
   - **Security**: Use signed URLs to control access to video files.

3. **Monitoring and Logging**:
   - Enable CloudFront access logs.
   - Use AWS CloudWatch to monitor performance metrics.

**Terraform Script**:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "video_bucket" {
  bucket = "my-video-content"
  acl    = "public-read"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-video-content/*"
    }
  ]
}
POLICY
}

resource "aws_cloudfront_distribution" "video_distribution" {
  origin {
    domain_name = aws_s3_bucket.video_bucket.bucket_regional_domain_name
    origin_id   = "myS3VideoOrigin"
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    target_origin_id       = "myS3VideoOrigin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = "arn:aws:acm:us-east-1:123456789012:certificate/your-certificate-id"
    ssl_support_method             = "sni-only"
  }
}
```

#### Example 3: API Acceleration

**Scenario**: A company wants to accelerate its API responses globally. The API is hosted on EC2 instances, and the company wants to use CloudFront to cache responses and reduce latency.

**Steps**:

1. **Set Up CloudFront Distribution**:
   - **Origin**: EC2 instances hosting the API.
   - **Viewer Protocol Policy**: Redirect HTTP to HTTPS.
   - **Cache Behavior**: Configure caching based on API responses (e.g., cache GET requests, not POST requests).
   - **SSL Configuration**: Use ACM for a custom SSL certificate.
   - **Security**: Use AWS WAF to protect against common API attacks.

2. **Monitoring and Logging**:
   - Enable CloudFront access logs.
   - Use AWS CloudWatch to monitor API performance metrics.

**Terraform Script**:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_cloudfront_distribution" "api_distribution" {
  origin {
    domain_name = "my-api.example.com"
    origin_id   = "myAPIOrigin"
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    target_origin_id       = "myAPIOrigin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }

    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 31536000
  }

  price_class = "PriceClass_All"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = "arn:aws:acm:us-east-1:123456789012:certificate/your-certificate-id"
    ssl_support_method             = "sni-only"
  }
}
```

### Conclusion

These real-world examples demonstrate how Amazon CloudFront can be used to deliver different types of content (static website content, streaming media, and API responses) globally with high performance and security. By following the steps outlined and using the provided Terraform scripts, you can set up CloudFront distributions tailored to your specific use case.
