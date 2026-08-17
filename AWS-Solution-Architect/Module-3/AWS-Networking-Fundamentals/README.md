## AWS Networking Fundamentals: Detailed Guide

### Introduction

AWS Networking Fundamentals is a critical aspect of cloud computing, enabling secure, reliable, and scalable communication between different components of a cloud infrastructure. This guide covers essential concepts, services, and best practices for networking in AWS.

### Table of Contents
1. **Introduction to AWS Networking**
    - Overview
    - Key Concepts

2. **Virtual Private Cloud (VPC)**
    - VPC Overview
    - Subnets
    - Route Tables
    - Internet Gateway
    - NAT Gateway
    - VPC Peering
    - VPC Endpoints

3. **Network Security**
    - Security Groups
    - Network ACLs
    - VPN Connections
    - AWS Transit Gateway

4. **Domain Name System (DNS)**
    - Amazon Route 53
    - DNS Management

5. **Load Balancing and Traffic Management**
    - Elastic Load Balancing (ELB)
    - Application Load Balancer (ALB)
    - Network Load Balancer (NLB)
    - Global Accelerator

6. **Content Delivery Network (CDN)**
    - Amazon CloudFront

7. **Monitoring and Troubleshooting**
    - VPC Flow Logs
    - AWS CloudTrail
    - AWS CloudWatch

8. **Hands-on Lab Exercises**
    - Setting up a VPC
    - Configuring Security Groups and NACLs
    - Setting up Load Balancers
    - Creating and Managing Route 53 DNS

9. **Best Practices and Design Patterns**

---

### 1. Introduction to AWS Networking

#### Overview
AWS networking services are designed to provide a scalable, secure, and highly available infrastructure for your applications. These services are integral to ensuring efficient communication and resource allocation in the cloud.

#### Key Concepts
- **VPC (Virtual Private Cloud):** A logically isolated section of the AWS cloud where you can launch AWS resources in a virtual network that you define.
- **Subnets:** Segments within a VPC that can host resources like EC2 instances.
- **Route Tables:** Control the traffic routing within a VPC.
- **Internet Gateway:** Enables communication between instances in a VPC and the internet.
- **Security Groups:** Virtual firewalls controlling inbound and outbound traffic at the instance level.
- **NACLs (Network Access Control Lists):** Provide subnet-level security.

---

### 2. Virtual Private Cloud (VPC)

#### VPC Overview
A VPC is a foundational element of AWS networking, allowing you to define a virtual network that closely resembles a traditional data center network.

#### Subnets
Subnets divide a VPC into smaller IP ranges:
- **Public Subnet:** Directly accessible from the internet.
- **Private Subnet:** No direct internet access, typically used for backend systems.

#### Route Tables
Route tables contain rules (routes) that determine where network traffic is directed:
- Main route table
- Custom route tables

#### Internet Gateway
An Internet Gateway allows resources in a VPC to access the internet and vice versa. 

#### NAT Gateway
NAT Gateways enable instances in a private subnet to connect to the internet or other AWS services but prevent the internet from initiating a connection with those instances.

#### VPC Peering
VPC Peering enables you to connect VPCs across the same or different AWS accounts, facilitating communication between resources in different VPCs.

#### VPC Endpoints
VPC Endpoints allow private connections between your VPC and supported AWS services without requiring an Internet Gateway, NAT device, VPN connection, or AWS Direct Connect.

---

### 3. Network Security

#### Security Groups
Security Groups act as virtual firewalls, controlling inbound and outbound traffic to AWS resources. They are stateful, meaning that if an incoming request is allowed, the outgoing response is automatically allowed.

#### Network ACLs
Network ACLs (NACLs) provide an additional layer of security at the subnet level. Unlike Security Groups, NACLs are stateless.

#### VPN Connections
VPN connections allow secure communication between your on-premises network and your AWS VPC.

#### AWS Transit Gateway
AWS Transit Gateway enables you to connect multiple VPCs and on-premises networks through a single gateway, simplifying network architecture and management.

---

### 4. Domain Name System (DNS)

#### Amazon Route 53
Amazon Route 53 is a scalable and highly available DNS and domain name registration service. It routes end users to internet applications by translating domain names into IP addresses.

#### DNS Management
Route 53 supports multiple routing policies such as simple, weighted, latency-based, failover, and geolocation routing.

---

### 5. Load Balancing and Traffic Management

#### Elastic Load Balancing (ELB)
ELB automatically distributes incoming application traffic across multiple targets, such as EC2 instances.

#### Application Load Balancer (ALB)
ALB is best suited for HTTP and HTTPS traffic and operates at the application layer (Layer 7).

#### Network Load Balancer (NLB)
NLB is designed for ultra-high performance and operates at the transport layer (Layer 4).

#### Global Accelerator
AWS Global Accelerator improves the availability and performance of your applications with global users by routing traffic to the optimal endpoint based on health, geography, and routing policies.

---

### 6. Content Delivery Network (CDN)

#### Amazon CloudFront
Amazon CloudFront is a global content delivery network (CDN) service that accelerates the delivery of your websites, APIs, video content, and other web assets.

---

### 7. Monitoring and Troubleshooting

#### VPC Flow Logs
VPC Flow Logs capture information about the IP traffic going to and from network interfaces in your VPC.

#### AWS CloudTrail
AWS CloudTrail provides a record of actions taken by a user, role, or an AWS service in your account, helping with compliance and auditing.

#### AWS CloudWatch
AWS CloudWatch monitors your AWS resources and applications in real time, providing system-wide visibility into resource utilization, application performance, and operational health.

---

### 8. Hands-on Lab Exercises

#### Setting up a VPC
- Create a VPC
- Add public and private subnets
- Configure route tables
- Attach an Internet Gateway

#### Configuring Security Groups and NACLs
- Create and configure Security Groups for EC2 instances
- Set up NACLs for subnets

#### Setting up Load Balancers
- Configure an Application Load Balancer for an EC2 instance

#### Creating and Managing Route 53 DNS
- Register a domain with Route 53
- Create hosted zones and records

---

### 9. Best Practices and Design Patterns
- Design for high availability and fault tolerance
- Implement least privilege access
- Use multi-tier architectures
- Automate infrastructure with Infrastructure as Code (IaC) using tools like AWS CloudFormation or Terraform

---

This guide provides a comprehensive overview of AWS networking fundamentals, designed to equip you with the knowledge and skills necessary to manage and optimize your AWS network infrastructure.



## Step-By-Step Guide on Setting up a VPC on AWS

### Introduction

Setting up a Virtual Private Cloud (VPC) in AWS allows you to create a logically isolated network within the AWS cloud. You can launch AWS resources such as EC2 instances into this VPC. This guide provides a detailed, step-by-step approach to setting up a VPC, including creating subnets, route tables, and configuring internet connectivity.

### Table of Contents

1. **Prerequisites**
2. **Creating a VPC**
3. **Creating Subnets**
4. **Creating and Associating Route Tables**
5. **Creating an Internet Gateway**
6. **Creating a NAT Gateway**
7. **Configuring Security Groups and Network ACLs**
8. **Launching EC2 Instances in the VPC**
9. **Verifying Connectivity**

---

### 1. Prerequisites

Before you begin, ensure you have:
- An AWS account
- Necessary permissions to create and manage VPCs, subnets, and other network resources
- AWS CLI installed (optional, for CLI-based setup)

---

### 2. Creating a VPC

1. **Open the VPC Console:**
   - Sign in to the AWS Management Console.
   - Open the VPC dashboard by navigating to **Services** > **VPC**.

2. **Create a VPC:**
   - Click on **Your VPCs** in the left-hand navigation pane.
   - Click on **Create VPC**.
   - Enter a **Name tag** for your VPC.
   - Provide a **CIDR block** (e.g., `10.0.0.0/16`).
   - Select **Tenancy** (default or dedicated).
   - Click **Create**.

---

### 3. Creating Subnets

1. **Create Public Subnet:**
   - Click on **Subnets** in the left-hand navigation pane.
   - Click on **Create Subnet**.
   - Select the **VPC** you just created.
   - Enter a **Subnet name** (e.g., `Public Subnet`).
   - Enter the **Availability Zone** (optional, to specify the zone).
   - Provide a **CIDR block** (e.g., `10.0.1.0/24`).
   - Click **Create**.

2. **Create Private Subnet:**
   - Repeat the above steps to create another subnet, this time naming it `Private Subnet` and using a different CIDR block (e.g., `10.0.2.0/24`).

---

### 4. Creating and Associating Route Tables

1. **Create a Route Table:**
   - Click on **Route Tables** in the left-hand navigation pane.
   - Click on **Create route table**.
   - Enter a **Name tag** for the route table (e.g., `Public Route Table`).
   - Select the **VPC** you created.
   - Click **Create**.

2. **Add Route to Route Table:**
   - Select the newly created route table.
   - Click on the **Routes** tab.
   - Click **Edit routes**.
   - Add a route with **Destination** `0.0.0.0/0` and **Target** set to your Internet Gateway (created in step 5).
   - Click **Save routes**.

3. **Associate Route Table with Subnet:**
   - Click on the **Subnet associations** tab.
   - Click **Edit subnet associations**.
   - Select your **Public Subnet**.
   - Click **Save associations**.

---

### 5. Creating an Internet Gateway

1. **Create Internet Gateway:**
   - Click on **Internet Gateways** in the left-hand navigation pane.
   - Click on **Create internet gateway**.
   - Enter a **Name tag** (e.g., `MyInternetGateway`).
   - Click **Create**.

2. **Attach Internet Gateway to VPC:**
   - Select the newly created Internet Gateway.
   - Click **Actions** > **Attach to VPC**.
   - Select your VPC.
   - Click **Attach internet gateway**.

---

### 6. Creating a NAT Gateway

1. **Allocate an Elastic IP Address:**
   - Click on **Elastic IPs** in the left-hand navigation pane.
   - Click on **Allocate Elastic IP address**.
   - Click **Allocate** and note the Elastic IP address.

2. **Create NAT Gateway:**
   - Click on **NAT Gateways** in the left-hand navigation pane.
   - Click on **Create NAT Gateway**.
   - Select your **Public Subnet**.
   - Select the **Elastic IP** you just allocated.
   - Click **Create NAT gateway**.

3. **Update Route Table for Private Subnet:**
   - Go back to **Route Tables**.
   - Create another route table for the private subnet (e.g., `Private Route Table`).
   - Add a route with **Destination** `0.0.0.0/0` and **Target** set to the NAT Gateway.
   - Associate this route table with your **Private Subnet**.

---

### 7. Configuring Security Groups and Network ACLs

1. **Create Security Groups:**
   - Click on **Security Groups** in the left-hand navigation pane.
   - Click on **Create security group**.
   - Enter a **Name** and **Description**.
   - Select your **VPC**.
   - Add inbound and outbound rules as needed (e.g., allowing SSH, HTTP, HTTPS).

2. **Create Network ACLs:**
   - Click on **Network ACLs** in the left-hand navigation pane.
   - Click on **Create network ACL**.
   - Enter a **Name** and select your **VPC**.
   - Add inbound and outbound rules (e.g., allowing traffic on specific ports).
   - Associate the NACL with the desired subnets.

---

### 8. Launching EC2 Instances in the VPC

1. **Launch an EC2 Instance:**
   - Navigate to **EC2 Dashboard** > **Instances**.
   - Click on **Launch Instance**.
   - Choose an AMI (Amazon Machine Image).
   - Choose an instance type.
   - Configure instance details:
     - Select your **VPC**.
     - Choose the **Subnet** (Public or Private).
     - Assign a public IP (for public subnet).
   - Add storage.
   - Add tags.
   - Configure security group (use the one created earlier).
   - Review and launch.

---

### 9. Verifying Connectivity

1. **Public Subnet Instance:**
   - Ensure the instance in the public subnet has a public IP.
   - Test connectivity by SSH-ing into the instance using the public IP.

2. **Private Subnet Instance:**
   - Ensure the instance in the private subnet does not have a public IP.
   - Test connectivity by SSH-ing into the public instance and then into the private instance from there.

---

By following this guide, you have successfully set up a VPC with public and private subnets, configured route tables, created an Internet Gateway and NAT Gateway, and launched EC2 instances within the VPC. This setup provides a robust foundation for building and deploying applications on AWS.


Below is a complete Terraform script for setting up a VPC with public and private subnets, an Internet Gateway, a NAT Gateway, route tables, and security groups. This script also includes the creation of EC2 instances in both subnets.

### Complete Terraform Script

```hcl
# Provider configuration
provider "aws" {
  region = "us-west-2"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

# Private Subnet
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "private-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-internet-gateway"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "main-nat-gateway"
  }
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-route-table"
  }
}

# Private Route Table
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "private-route-table"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# Security Group
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-sg"
  }
}

# EC2 Instances
resource "aws_instance" "public" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web.name]

  tags = {
    Name = "public-instance"
  }
}

resource "aws_instance" "private" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.private.id
  security_groups = [aws_security_group.web.name]

  tags = {
    Name = "private-instance"
  }
}

# Outputs
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "private_subnet_id" {
  value = aws_subnet.private.id
}

output "public_instance_id" {
  value = aws_instance.public.id
}

output "private_instance_id" {
  value = aws_instance.private.id
}
```

### How to Use the Script

1. **Install Terraform:**
   - Follow the instructions on the [Terraform website](https://www.terraform.io/downloads) to install Terraform.

2. **Configure AWS Credentials:**
   - Ensure you have your AWS credentials configured. You can do this by setting environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) or by using the AWS CLI to configure credentials.

3. **Save the Script:**
   - Save the above script to a file named `main.tf`.

4. **Initialize Terraform:**
   ```bash
   terraform init
   ```

5. **Validate Configuration:**
   ```bash
   terraform validate
   ```

6. **Apply the Configuration:**
   ```bash
   terraform apply
   ```
   - Confirm the apply by typing `yes` when prompted.

7. **Verify Resources:**
   - After the apply command completes, you can check the AWS Management Console to verify that the VPC, subnets, route tables, Internet Gateway, NAT Gateway, and EC2 instances have been created.

### Notes

- Adjust the `ami` value in the `aws_instance` resource to use a valid AMI ID for your region.
- Modify security group rules and instance tags as needed.
- This script uses a minimal configuration for demonstration purposes. In a production environment, you may need additional configurations and security settings.


## Step-by-Step Guide on Configuring Security Groups and Network ACLs (NACLs) in AWS

### Introduction

Security Groups and Network ACLs (NACLs) are fundamental components for managing network security in AWS. Security Groups act as virtual firewalls for instances, controlling inbound and outbound traffic. Network ACLs provide an additional layer of security at the subnet level. This guide provides a detailed step-by-step process for configuring both Security Groups and NACLs.

### Table of Contents
1. **Understanding Security Groups and NACLs**
    - Security Groups
    - Network ACLs

2. **Configuring Security Groups**
    - Creating a Security Group
    - Adding Rules to a Security Group
    - Associating Security Groups with Instances

3. **Configuring Network ACLs**
    - Creating a Network ACL
    - Adding Rules to a Network ACL
    - Associating Network ACLs with Subnets

4. **Best Practices**

5. **Hands-on Lab Exercises**

---

### 1. Understanding Security Groups and NACLs

#### Security Groups
- **Function:** Act as a virtual firewall for EC2 instances, controlling inbound and outbound traffic.
- **Scope:** Instance-level.
- **State:** Stateful (automatically allows return traffic).
- **Rules:** Allow rules only.

#### Network ACLs
- **Function:** Provide an additional layer of security at the subnet level, controlling inbound and outbound traffic.
- **Scope:** Subnet-level.
- **State:** Stateless (does not automatically allow return traffic).
- **Rules:** Allow and deny rules.

---

### 2. Configuring Security Groups

#### Creating a Security Group

1. **Navigate to the EC2 Dashboard:**
   - Open the AWS Management Console.
   - Navigate to the EC2 Dashboard.

2. **Create a Security Group:**
   - In the left navigation pane, click on "Security Groups" under "Network & Security."
   - Click on "Create security group."

3. **Configure the Security Group:**
   - **Name:** Enter a name for the security group (e.g., `MySecurityGroup`).
   - **Description:** Provide a description for the security group.
   - **VPC:** Select the VPC where the security group will be used.

4. **Add Inbound Rules:**
   - Click on "Add Rule."
   - **Type:** Select the type of traffic (e.g., HTTP).
   - **Protocol:** Select the protocol (e.g., TCP).
   - **Port Range:** Specify the port range (e.g., 80).
   - **Source:** Define the source IP or CIDR (e.g., `0.0.0.0/0` for all IPs).
   - Repeat for additional rules as needed.

5. **Add Outbound Rules:**
   - Click on "Add Rule."
   - **Type:** Select the type of traffic.
   - **Protocol:** Select the protocol.
   - **Port Range:** Specify the port range.
   - **Destination:** Define the destination IP or CIDR.
   - Repeat for additional rules as needed.

6. **Create the Security Group:**
   - Review the rules.
   - Click on "Create security group."

#### Associating Security Groups with Instances

1. **Launch an EC2 Instance:**
   - Navigate to the EC2 Dashboard.
   - Click on "Launch Instance."
   - Follow the wizard to configure the instance.

2. **Assign the Security Group:**
   - In the "Configure Security Group" step, select "Select an existing security group."
   - Choose the security group you created (e.g., `MySecurityGroup`).
   - Complete the instance launch process.

3. **Modify Security Group for Running Instances:**
   - Navigate to the EC2 Dashboard.
   - Select the running instance.
   - Click on "Actions," then "Security," and select "Change security groups."
   - Choose the desired security group and click "Assign security groups."

---

### 3. Configuring Network ACLs

#### Creating a Network ACL

1. **Navigate to the VPC Dashboard:**
   - Open the AWS Management Console.
   - Navigate to the VPC Dashboard.

2. **Create a Network ACL:**
   - In the left navigation pane, click on "Network ACLs."
   - Click on "Create Network ACL."

3. **Configure the Network ACL:**
   - **Name:** Enter a name for the network ACL (e.g., `MyNetworkACL`).
   - **VPC:** Select the VPC where the network ACL will be used.
   - Click "Create."

#### Adding Rules to a Network ACL

1. **Add Inbound Rules:**
   - Select the network ACL.
   - Click on the "Inbound Rules" tab.
   - Click on "Edit Inbound Rules."
   - **Rule Number:** Enter a rule number (e.g., 100).
   - **Type:** Select the type of traffic (e.g., HTTP).
   - **Protocol:** Select the protocol (e.g., TCP).
   - **Port Range:** Specify the port range (e.g., 80).
   - **Source:** Define the source IP or CIDR (e.g., `0.0.0.0/0` for all IPs).
   - **Allow/Deny:** Choose whether to allow or deny the traffic.
   - Repeat for additional rules as needed.
   - Click "Save changes."

2. **Add Outbound Rules:**
   - Select the network ACL.
   - Click on the "Outbound Rules" tab.
   - Click on "Edit Outbound Rules."
   - **Rule Number:** Enter a rule number.
   - **Type:** Select the type of traffic.
   - **Protocol:** Select the protocol.
   - **Port Range:** Specify the port range.
   - **Destination:** Define the destination IP or CIDR.
   - **Allow/Deny:** Choose whether to allow or deny the traffic.
   - Repeat for additional rules as needed.
   - Click "Save changes."

#### Associating Network ACLs with Subnets

1. **Select a Subnet:**
   - Navigate to the VPC Dashboard.
   - Click on "Subnets."
   - Select the subnet you want to associate with the network ACL.

2. **Modify Network ACL Association:**
   - Click on the "Actions" dropdown menu.
   - Select "Edit network ACL association."
   - Choose the network ACL you created (e.g., `MyNetworkACL`).
   - Click "Save."

---

### 4. Best Practices

- **Least Privilege:** Apply the principle of least privilege by allowing only the necessary traffic.
- **Segmentation:** Use separate Security Groups and NACLs for different application tiers.
- **Monitoring:** Enable VPC Flow Logs to monitor traffic and detect anomalies.
- **Auditing:** Regularly review and audit Security Group and NACL rules.
- **Automation:** Use IaC tools like CloudFormation or Terraform to manage Security Groups and NACLs.

---

### 5. Hands-on Lab Exercises

#### Lab 1: Configuring Security Groups
1. Create a Security Group for web servers.
2. Add rules to allow HTTP (port 80) and HTTPS (port 443) traffic from the internet.
3. Launch an EC2 instance and associate it with the Security Group.

#### Lab 2: Configuring Network ACLs
1. Create a Network ACL for a public subnet.
2. Add rules to allow HTTP and HTTPS traffic inbound and outbound.
3. Associate the Network ACL with a public subnet.

#### Lab 3: Monitoring and Auditing
1. Enable VPC Flow Logs for the VPC.
2. Review the logs in CloudWatch to identify allowed and denied traffic.
3. Audit the Security Group and NACL rules to ensure compliance with security policies.

---

By following this step-by-step guide, you can effectively configure and manage Security Groups and Network ACLs in AWS, ensuring robust network security for your cloud infrastructure.


Here are Terraform scripts for configuring a Security Group and a Network ACL in AWS. These scripts include setting up a VPC, subnets, a security group, and a network ACL.

### Terraform Script for VPC, Subnets, Security Group, and Network ACL

#### 1. VPC and Subnets

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "private-subnet"
  }
}
```

#### 2. Security Group

```hcl
resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow inbound HTTP and HTTPS traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-sg"
  }
}
```

#### 3. Network ACL

```hcl
resource "aws_network_acl" "public_acl" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "public-acl"
  }
}

resource "aws_network_acl_rule" "allow_http_inbound" {
  network_acl_id = aws_network_acl.public_acl.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 80
  to_port        = 80
}

resource "aws_network_acl_rule" "allow_https_inbound" {
  network_acl_id = aws_network_acl.public_acl.id
  rule_number    = 110
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 443
  to_port        = 443
}

resource "aws_network_acl_rule" "allow_all_outbound" {
  network_acl_id = aws_network_acl.public_acl.id
  rule_number    = 100
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}

resource "aws_subnet_network_acl_association" "public_acl_association" {
  subnet_id     = aws_subnet.public.id
  network_acl_id = aws_network_acl.public_acl.id
}
```

#### 4. Launch an EC2 Instance

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0" # Replace with your desired AMI ID
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.name]

  tags = {
    Name = "web-instance"
  }
}
```

### Complete Terraform Script

Below is the complete script combining all the components:

```hcl
provider "aws" {
  region = "us-west-2"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

# Subnets
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "private-subnet"
  }
}

# Security Group
resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow inbound HTTP and HTTPS traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-sg"
  }
}

# Network ACL
resource "aws_network_acl" "public_acl" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "public-acl"
  }
}

resource "aws_network_acl_rule" "allow_http_inbound" {
  network_acl_id = aws_network_acl.public_acl.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 80
  to_port        = 80
}

resource "aws_network_acl_rule" "allow_https_inbound" {
  network_acl_id = aws_network_acl.public_acl.id
  rule_number    = 110
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 443
  to_port        = 443
}

resource "aws_network_acl_rule" "allow_all_outbound" {
  network_acl_id = aws_network_acl.public_acl.id
  rule_number    = 100
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}

resource "aws_subnet_network_acl_association" "public_acl_association" {
  subnet_id     = aws_subnet.public.id
  network_acl_id = aws_network_acl.public_acl.id
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0" # Replace with your desired AMI ID
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.name]

  tags = {
    Name = "web-instance"
  }
}
```

### Instructions to Apply the Script

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Validate the Configuration:**
   ```bash
   terraform validate
   ```

3. **Apply the Configuration:**
   ```bash
   terraform apply
   ```

4. **Destroy the Infrastructure (if needed):**
   ```bash
   terraform destroy
   ```

By following these steps and using the provided scripts, you can effectively configure a VPC, subnets, security groups, and network ACLs in AWS using Terraform.


## Step-by-Step Guide on Setting up Load Balancers in AWS

### Table of Contents
1. **Introduction to Load Balancers**
2. **Types of Load Balancers in AWS**
3. **Setting up an Application Load Balancer (ALB)**
    - Step 1: Create Target Groups
    - Step 2: Launch EC2 Instances
    - Step 3: Create the Application Load Balancer
    - Step 4: Configure Listener and Rules
    - Step 5: Register Targets
    - Step 6: Test the Load Balancer
4. **Setting up a Network Load Balancer (NLB)**
    - Step 1: Create Target Groups
    - Step 2: Launch EC2 Instances
    - Step 3: Create the Network Load Balancer
    - Step 4: Configure Listener and Rules
    - Step 5: Register Targets
    - Step 6: Test the Load Balancer
5. **Best Practices for Load Balancers**

---

### 1. Introduction to Load Balancers

Load balancers distribute incoming application or network traffic across multiple targets, such as EC2 instances, containers, or IP addresses, to ensure high availability and reliability. AWS offers different types of load balancers to suit various needs.

### 2. Types of Load Balancers in AWS

- **Application Load Balancer (ALB):** Operates at the application layer (Layer 7) and is best suited for HTTP/HTTPS traffic.
- **Network Load Balancer (NLB):** Operates at the transport layer (Layer 4) and is designed for high-performance and low-latency traffic.
- **Classic Load Balancer (CLB):** Operates at both the transport layer (Layer 4) and application layer (Layer 7), but is being phased out in favor of ALB and NLB.

---

### 3. Setting up an Application Load Balancer (ALB)

#### Step 1: Create Target Groups

1. **Navigate to the EC2 Dashboard:**
   - Open the AWS Management Console.
   - Navigate to the EC2 Dashboard.

2. **Create Target Group:**
   - On the left sidebar, click "Target Groups."
   - Click "Create target group."
   - Choose "Instances" as the target type.
   - Set the target group name (e.g., `my-alb-target-group`).
   - Select the protocol and port (e.g., HTTP, port 80).
   - Configure health checks (default is HTTP, path `/`).
   - Click "Next" and then "Create target group."

#### Step 2: Launch EC2 Instances

1. **Launch Instances:**
   - Launch at least two EC2 instances in different availability zones.
   - Ensure the instances are in the same VPC as the ALB.

2. **Install Web Server (Optional):**
   - Connect to each EC2 instance and install a web server (e.g., Apache, Nginx).
   - Ensure the web server is running and serving a test page.

#### Step 3: Create the Application Load Balancer

1. **Navigate to the Load Balancers Section:**
   - On the EC2 Dashboard, click "Load Balancers" in the left sidebar.
   - Click "Create Load Balancer."

2. **Select Application Load Balancer:**
   - Choose "Application Load Balancer."
   - Click "Create."

3. **Configure Load Balancer:**
   - Name your load balancer (e.g., `my-application-load-balancer`).
   - Choose the scheme (internet-facing or internal).
   - Select the IP address type (IPv4 or dualstack).
   - Choose the VPC and select at least two availability zones and subnets.

4. **Configure Security Settings:**
   - For HTTP, no SSL certificates are needed. For HTTPS, select or create an SSL certificate.
   - Configure security groups to allow inbound traffic on port 80 (HTTP) or port 443 (HTTPS).

#### Step 4: Configure Listener and Rules

1. **Add Listener:**
   - By default, an HTTP listener is added. You can add an HTTPS listener if needed.
   - Click "Add listener" to add another protocol/port if required.

2. **Configure Listener Rules:**
   - Add rules to forward traffic to your target group created in Step 1.
   - Review and adjust any default rules as necessary.

#### Step 5: Register Targets

1. **Register EC2 Instances:**
   - Select the target group created in Step 1.
   - Click "Register targets."
   - Choose the EC2 instances you launched.
   - Click "Include as pending below" and then "Register pending targets."

#### Step 6: Test the Load Balancer

1. **Obtain DNS Name:**
   - Go to the "Load Balancers" section.
   - Select your ALB and note the DNS name provided.

2. **Test the ALB:**
   - Open a web browser and enter the DNS name.
   - You should see the test page from one of your EC2 instances, indicating the ALB is distributing traffic correctly.

---

### 4. Setting up a Network Load Balancer (NLB)

#### Step 1: Create Target Groups

1. **Navigate to the EC2 Dashboard:**
   - Open the AWS Management Console.
   - Navigate to the EC2 Dashboard.

2. **Create Target Group:**
   - On the left sidebar, click "Target Groups."
   - Click "Create target group."
   - Choose "Instances" as the target type.
   - Set the target group name (e.g., `my-nlb-target-group`).
   - Select the protocol and port (e.g., TCP, port 80).
   - Configure health checks (default is TCP).
   - Click "Next" and then "Create target group."

#### Step 2: Launch EC2 Instances

1. **Launch Instances:**
   - Launch at least two EC2 instances in different availability zones.
   - Ensure the instances are in the same VPC as the NLB.

2. **Configure Services (Optional):**
   - Ensure the services running on the instances are listening on the ports specified in the target group.

#### Step 3: Create the Network Load Balancer

1. **Navigate to the Load Balancers Section:**
   - On the EC2 Dashboard, click "Load Balancers" in the left sidebar.
   - Click "Create Load Balancer."

2. **Select Network Load Balancer:**
   - Choose "Network Load Balancer."
   - Click "Create."

3. **Configure Load Balancer:**
   - Name your load balancer (e.g., `my-network-load-balancer`).
   - Choose the scheme (internet-facing or internal).
   - Select the IP address type (IPv4 or dualstack).
   - Choose the VPC and select at least two availability zones and subnets.

#### Step 4: Configure Listener and Rules

1. **Add Listener:**
   - By default, a TCP listener is added. Add other listeners if needed.

2. **Configure Listener Rules:**
   - Add rules to forward traffic to your target group created in Step 1.
   - Review and adjust any default rules as necessary.

#### Step 5: Register Targets

1. **Register EC2 Instances:**
   - Select the target group created in Step 1.
   - Click "Register targets."
   - Choose the EC2 instances you launched.
   - Click "Include as pending below" and then "Register pending targets."

#### Step 6: Test the Load Balancer

1. **Obtain DNS Name:**
   - Go to the "Load Balancers" section.
   - Select your NLB and note the DNS name provided.

2. **Test the NLB:**
   - Open a web browser and enter the DNS name (or use a TCP client if using non-HTTP protocols).
   - Ensure the traffic is correctly routed to your EC2 instances.

---

### 5. Best Practices for Load Balancers

- **Use Health Checks:** Ensure health checks are properly configured to monitor the health of your targets and avoid routing traffic to unhealthy instances.
- **Enable Cross-Zone Load Balancing:** This helps distribute traffic evenly across all registered instances in all enabled availability zones.
- **Use Appropriate Load Balancer Types:** Choose the right type of load balancer based on your application's needs (e.g., ALB for HTTP/HTTPS, NLB for TCP/UDP).
- **Secure Your Load Balancer:** Use security groups and network ACLs to restrict access to your load balancer. For ALBs, use SSL/TLS to encrypt traffic.
- **Monitor Performance:** Use AWS CloudWatch to monitor the performance and metrics of your load balancer.
- **Automate Scaling:** Configure Auto Scaling to dynamically adjust the number of instances based on traffic demand.

By following these steps and best practices, you can effectively set up and manage load balancers in AWS, ensuring high availability, reliability, and scalability for your applications.


### Terraform Scripts for Setting up Load Balancers in AWS

This section provides Terraform scripts for setting up both an Application Load Balancer (ALB) and a Network Load Balancer (NLB) in AWS.

---

### Application Load Balancer (ALB) Setup

#### Step 1: Initialize Terraform

Create a directory for your Terraform files and initialize Terraform.

```bash
mkdir terraform-alb-setup
cd terraform-alb-setup
terraform init
```

#### Step 2: Create `main.tf` File

Create a `main.tf` file with the following content:

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index}"
  }
}

resource "aws_security_group" "alb_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-sg"
  }
}

resource "aws_instance" "web" {
  count = 2
  ami = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id = element(aws_subnet.public[*].id, count.index)
  security_groups = ["${aws_security_group.alb_sg.name}"]

  tags = {
    Name = "web-instance-${count.index}"
  }

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World!" > /var/www/html/index.html
              yum install -y httpd
              service httpd start
              chkconfig httpd on
              EOF
}

resource "aws_lb" "app" {
  name               = "app-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = aws_subnet.public[*].id

  tags = {
    Name = "app-load-balancer"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "app-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    path                = "/"
    interval            = 30
    matcher             = "200"
  }

  tags = {
    Name = "app-target-group"
  }
}

resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

resource "aws_lb_target_group_attachment" "app" {
  count            = 2
  target_group_arn = aws_lb_target_group.app.arn
  target_id        = element(aws_instance.web[*].id, count.index)
  port             = 80
}
```

#### Step 3: Apply the Configuration

```bash
terraform apply
```

This script sets up an ALB with two EC2 instances as targets in a public subnet.

---

### Network Load Balancer (NLB) Setup

#### Step 1: Initialize Terraform

Create a directory for your Terraform files and initialize Terraform.

```bash
mkdir terraform-nlb-setup
cd terraform-nlb-setup
terraform init
```

#### Step 2: Create `main.tf` File

Create a `main.tf` file with the following content:

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index}"
  }
}

resource "aws_security_group" "nlb_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "nlb-sg"
  }
}

resource "aws_instance" "web" {
  count = 2
  ami = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id = element(aws_subnet.public[*].id, count.index)
  security_groups = ["${aws_security_group.nlb_sg.name}"]

  tags = {
    Name = "web-instance-${count.index}"
  }

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World!" > /var/www/html/index.html
              yum install -y httpd
              service httpd start
              chkconfig httpd on
              EOF
}

resource "aws_lb" "network" {
  name               = "network-load-balancer"
  internal           = false
  load_balancer_type = "network"
  subnets            = aws_subnet.public[*].id

  tags = {
    Name = "network-load-balancer"
  }
}

resource "aws_lb_target_group" "network" {
  name     = "network-target-group"
  port     = 80
  protocol = "TCP"
  vpc_id   = aws_vpc.main.id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 10
    interval            = 30
    protocol            = "TCP"
  }

  tags = {
    Name = "network-target-group"
  }
}

resource "aws_lb_listener" "network" {
  load_balancer_arn = aws_lb.network.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.network.arn
  }
}

resource "aws_lb_target_group_attachment" "network" {
  count            = 2
  target_group_arn = aws_lb_target_group.network.arn
  target_id        = element(aws_instance.web[*].id, count.index)
  port             = 80
}
```

#### Step 3: Apply the Configuration

```bash
terraform apply
```

This script sets up an NLB with two EC2 instances as targets in a public subnet.

---

These Terraform scripts automate the setup of Application Load Balancers and Network Load Balancers in AWS, providing high availability and scalability for your applications.



## Step-by-Step Guide on Creating and Managing Route 53 DNS

Amazon Route 53 is a scalable and highly available Domain Name System (DNS) web service designed to route end-users to internet applications by translating human-readable names (like www.example.com) into the numeric IP addresses (like 192.0.2.1) that computers use to connect to each other. This guide will take you through the steps of creating and managing DNS records using Route 53.

### Table of Contents

1. **Setting Up Amazon Route 53**
    - Creating a Hosted Zone
    - Understanding DNS Records

2. **Managing DNS Records**
    - Creating and Modifying Records
    - Common Record Types
    - TTL (Time to Live) Settings

3. **Routing Policies**
    - Simple Routing
    - Weighted Routing
    - Latency-based Routing
    - Failover Routing
    - Geolocation Routing
    - Multi-value Answer Routing

4. **Monitoring and Troubleshooting**
    - Health Checks
    - DNS Query Logging

5. **Best Practices**

---

### 1. Setting Up Amazon Route 53

#### Creating a Hosted Zone

1. **Sign in to the AWS Management Console:**
   - Open the [Route 53 console](https://console.aws.amazon.com/route53/).

2. **Create a Hosted Zone:**
   - Click on "Hosted zones" in the navigation pane.
   - Click on "Create hosted zone."
   - Enter the domain name (e.g., example.com).
   - Choose the type of hosted zone (Public or Private).
     - **Public Hosted Zone:** Used to route internet traffic to your resources.
     - **Private Hosted Zone:** Used to route traffic within an Amazon VPC.
   - Click "Create."

3. **Note the Nameservers:**
   - After creating the hosted zone, note the nameservers (NS records) provided by Route 53. You'll need to update your domain's registrar to use these nameservers.

#### Understanding DNS Records

- **DNS Records:** Entries in a DNS database that provide information about a domain and its associated services.
- **Types of Records:** Common types include A, AAAA, CNAME, MX, TXT, and NS records.

---

### 2. Managing DNS Records

#### Creating and Modifying Records

1. **Navigate to Hosted Zone:**
   - In the Route 53 console, click on the hosted zone you created.

2. **Create a Record Set:**
   - Click on "Create record."
   - Enter the record name (e.g., www).
   - Select the record type (A, AAAA, CNAME, etc.).
   - Enter the value (e.g., IP address for an A record).
   - Set the TTL (Time to Live).
   - Choose a routing policy (default is Simple routing).
   - Click "Create records."

3. **Modify an Existing Record:**
   - Select the record you want to modify from the hosted zone.
   - Click "Edit record."
   - Make the necessary changes and click "Save changes."

#### Common Record Types

- **A Record:** Maps a domain name to an IPv4 address.
- **AAAA Record:** Maps a domain name to an IPv6 address.
- **CNAME Record:** Maps an alias name to another domain name.
- **MX Record:** Specifies mail servers for a domain.
- **TXT Record:** Provides text information to sources outside your domain.
- **NS Record:** Indicates the nameservers for the domain.

#### TTL (Time to Live) Settings

- **TTL:** Specifies the duration (in seconds) that DNS resolvers cache the DNS record before querying Route 53 again. Common TTL values are 300 seconds (5 minutes), 3600 seconds (1 hour), or 86400 seconds (24 hours).

---

### 3. Routing Policies

#### Simple Routing

- **Simple Routing:** Routes traffic to a single resource. Use when you have a single resource performing a given function for your domain.

#### Weighted Routing

- **Weighted Routing:** Distributes traffic across multiple resources based on assigned weights. Useful for load balancing and A/B testing.
  - **Example:** 70% traffic to resource A, 30% to resource B.

#### Latency-based Routing

- **Latency-based Routing:** Routes traffic to the resource with the lowest latency to the user. Helps improve performance by reducing response times.

#### Failover Routing

- **Failover Routing:** Routes traffic to a primary resource unless it is unhealthy, in which case it routes traffic to a secondary resource. Requires health checks.

#### Geolocation Routing

- **Geolocation Routing:** Routes traffic based on the geographic location of the user. Useful for serving localized content.

#### Multi-value Answer Routing

- **Multi-value Answer Routing:** Returns multiple values, such as IP addresses, in response to DNS queries. Can be used for simple load balancing and health checking.

---

### 4. Monitoring and Troubleshooting

#### Health Checks

- **Health Checks:** Monitor the health and performance of your application endpoints. You can configure Route 53 to perform health checks on resources and redirect traffic if an endpoint is unhealthy.
  - **Create Health Check:**
    - In the Route 53 console, click on "Health checks."
    - Click "Create health check."
    - Configure the health check (protocol, endpoint, port, etc.).
    - Click "Create."

#### DNS Query Logging

- **DNS Query Logging:** Enables logging of DNS queries received by Route 53. Useful for monitoring and troubleshooting DNS issues.
  - **Enable Query Logging:**
    - In the Route 53 console, click on "Configure query logging."
    - Select the hosted zone.
    - Choose the CloudWatch Logs log group where the logs will be sent.
    - Click "Configure query logging."

---

### 5. Best Practices

- **Use TTLs Appropriately:** Set appropriate TTL values to balance between performance (low TTL) and reduced query costs (high TTL).
- **Leverage Multiple Routing Policies:** Combine routing policies to meet complex routing requirements.
- **Monitor Health Checks:** Regularly monitor and update health checks to ensure failover mechanisms work as expected.
- **Secure Your Domains:** Use DNSSEC (Domain Name System Security Extensions) to add an extra layer of security to your domains.
- **Automate with Infrastructure as Code (IaC):** Use tools like AWS CloudFormation or Terraform to manage Route 53 configurations programmatically.

---

By following this step-by-step guide, you can effectively create and manage DNS records using Amazon Route 53, ensuring high availability, performance, and reliability for your domain and associated services.


Below are Terraform scripts to set up DNS management using Amazon Route 53. This includes creating a hosted zone, adding different types of DNS records, and configuring health checks.

### 1. Setting Up a Hosted Zone

Create a `main.tf` file and add the following code to set up a hosted zone in Route 53:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_route53_zone" "example" {
  name = "example.com"
}
```

### 2. Adding DNS Records

You can add various DNS records to your hosted zone by appending the following code to your `main.tf` file.

#### A Record

```hcl
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = "300"
  records = ["192.0.2.1"]
}
```

#### CNAME Record

```hcl
resource "aws_route53_record" "blog" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "blog.example.com"
  type    = "CNAME"
  ttl     = "300"
  records = ["example.com"]
}
```

#### MX Record

```hcl
resource "aws_route53_record" "mail" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "example.com"
  type    = "MX"
  ttl     = "300"
  records = ["10 mail.example.com"]
}
```

#### TXT Record

```hcl
resource "aws_route53_record" "txt" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "example.com"
  type    = "TXT"
  ttl     = "300"
  records = ["v=spf1 include:example.com ~all"]
}
```

### 3. Configuring Health Checks

#### Create Health Check

```hcl
resource "aws_route53_health_check" "example" {
  fqdn              = "www.example.com"
  port              = 80
  type              = "HTTP"
  resource_path     = "/"
  failure_threshold = 3
}
```

#### Associate Health Check with DNS Record

```hcl
resource "aws_route53_record" "www_health_checked" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = "300"
  records = ["192.0.2.1"]

  health_check_id = aws_route53_health_check.example.id
}
```

### 4. Using Routing Policies

#### Weighted Routing Policy

```hcl
resource "aws_route53_record" "weighted_example1" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "example.com"
  type    = "A"
  ttl     = "300"
  records = ["192.0.2.1"]

  set_identifier = "example1"
  weight         = 70
}

resource "aws_route53_record" "weighted_example2" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "example.com"
  type    = "A"
  ttl     = "300"
  records = ["192.0.2.2"]

  set_identifier = "example2"
  weight         = 30
}
```

#### Latency-based Routing Policy

```hcl
resource "aws_route53_record" "latency_example_us" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "example.com"
  type    = "A"
  ttl     = "300"
  records = ["192.0.2.1"]

  set_identifier   = "us-east-1"
  latency_routing_policy = {
    region = "us-east-1"
  }
}

resource "aws_route53_record" "latency_example_eu" {
  zone_id = aws_route53_zone.example.zone_id
  name    = "example.com"
  type    = "A"
  ttl     = "300"
  records = ["192.0.2.2"]

  set_identifier   = "eu-west-1"
  latency_routing_policy = {
    region = "eu-west-1"
  }
}
```

### 5. Applying the Configuration

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Validate the Configuration:**
   ```bash
   terraform validate
   ```

3. **Apply the Configuration:**
   ```bash
   terraform apply
   ```

4. **Destroy the Configuration:**
   If you need to remove the resources:
   ```bash
   terraform destroy
   ```

This Terraform configuration sets up a hosted zone, various DNS records, health checks, and different routing policies using Amazon Route 53. Adjust the values as needed to fit your specific use case.
