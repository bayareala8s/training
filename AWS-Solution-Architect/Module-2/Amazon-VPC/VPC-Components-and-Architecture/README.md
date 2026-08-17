### Detailed Guide for Amazon VPC Components and Architecture

#### 1. **Amazon VPC Overview**

Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources in a logically isolated virtual network that you define. This section provides a detailed guide on VPC components and how they fit into an overall architecture.

#### 2. **VPC Components**

1. **VPC**
   - A virtual network dedicated to your AWS account. You can specify an IPv4 address range (CIDR block) for your VPC (e.g., 10.0.0.0/16).

2. **Subnets**
   - Subnets are segments of a VPC's IP address range where you can place groups of isolated resources. You can create both public and private subnets.
     - **Public Subnet**: A subnet that has a route to an internet gateway.
     - **Private Subnet**: A subnet that doesn't have a route to the internet gateway but can access the internet via a NAT gateway/instance.

3. **Route Tables**
   - A set of rules (routes) that are used to determine where network traffic is directed. Each subnet in your VPC must be associated with a route table.

4. **Internet Gateway**
   - A horizontally scaled, redundant, and highly available VPC component that allows communication between instances in your VPC and the internet.

5. **NAT Gateway and NAT Instances**
   - **NAT Gateway**: A managed service that enables instances in a private subnet to connect to the internet.
   - **NAT Instance**: An Amazon EC2 instance that performs the same function as a NAT Gateway.

6. **Security Groups**
   - Virtual firewalls that control inbound and outbound traffic to your instances. Security groups act at the instance level.

7. **Network ACLs (Access Control Lists)**
   - An optional layer of security that acts at the subnet level, controlling inbound and outbound traffic for the subnet.

8. **VPC Peering**
   - A networking connection between two VPCs that enables instances in either VPC to communicate as if they are within the same network.

9. **VPN and AWS Direct Connect**
   - **VPN**: Establishes a secure connection between your on-premises network and your VPC.
   - **AWS Direct Connect**: Provides a dedicated network connection from your premises to AWS.

10. **VPC Endpoints**
    - Enable private connections between your VPC and supported AWS services without requiring an Internet Gateway, NAT device, VPN connection, or AWS Direct Connect.

#### 3. **Building a Sample VPC Architecture**

Let's build a VPC architecture for a sample web application.

**Step 1: Create a VPC**

1. Sign in to the AWS Management Console.
2. Navigate to the VPC Dashboard.
3. Click on "Create VPC."
4. Specify the IPv4 CIDR block (e.g., 10.0.0.0/16).
5. Choose tenancy (default or dedicated).
6. Click on "Create."

**Step 2: Create Subnets**

1. Navigate to the "Subnets" section in the VPC Dashboard.
2. Click on "Create subnet."
3. Select the VPC you created.
4. Specify the subnet name, Availability Zone, and IPv4 CIDR block (e.g., 10.0.1.0/24 for public, 10.0.2.0/24 for private).
5. Create both public and private subnets.

**Step 3: Create an Internet Gateway**

1. Navigate to the "Internet Gateways" section.
2. Click on "Create internet gateway."
3. Attach the internet gateway to your VPC.

**Step 4: Configure Route Tables**

1. Navigate to the "Route Tables" section.
2. Create a new route table for the public subnet.
   - Add a route that directs internet traffic (0.0.0.0/0) to the internet gateway.
3. Associate the public subnet with this route table.
4. Create a route table for the private subnet.
   - Add a route that directs internet traffic to a NAT Gateway (to be created in Step 5).

**Step 5: Create a NAT Gateway**

1. Navigate to the "NAT Gateways" section.
2. Click on "Create NAT gateway."
3. Select the public subnet and allocate an Elastic IP address.
4. Update the private subnet's route table to direct internet traffic (0.0.0.0/0) to the NAT Gateway.

**Step 6: Configure Security Groups**

1. Navigate to the "Security Groups" section.
2. Create a security group for your web servers.
   - Allow inbound HTTP (port 80) and HTTPS (port 443) traffic from anywhere (0.0.0.0/0).
   - Allow inbound SSH traffic from your IP address.
3. Create a security group for your application servers.
   - Allow inbound traffic from the web server security group.
4. Create a security group for your database servers.
   - Allow inbound traffic from the application server security group.

**Step 7: Launch Instances**

1. Launch EC2 instances in the public subnet for your web servers.
2. Launch EC2 instances in the private subnet for your application servers and databases.
3. Associate the appropriate security groups with each instance.

**Step 8: Additional Configuration (Optional)**

1. **VPC Peering**: If you have multiple VPCs and need communication between them, set up VPC peering.
2. **VPN and Direct Connect**: For secure and high-performance connections between your on-premises network and AWS, set up VPN or Direct Connect.
3. **VPC Endpoints**: Create VPC endpoints for services like S3 to enable private connectivity.

#### 4. **Example Architecture Diagram**

**Components**:
- **VPC**: 10.0.0.0/16
- **Public Subnets**: 10.0.1.0/24 (AZ1), 10.0.3.0/24 (AZ2)
- **Private Subnets**: 10.0.2.0/24 (AZ1), 10.0.4.0/24 (AZ2)
- **Internet Gateway**: igw-12345678
- **NAT Gateway**: nat-12345678
- **Route Tables**: 
  - Public Route Table (rtb-public) with a route to IGW.
  - Private Route Table (rtb-private) with a route to NAT.
- **Security Groups**:
  - Web SG: Allows HTTP, HTTPS, and SSH.
  - App SG: Allows traffic from Web SG.
  - DB SG: Allows traffic from App SG.
- **EC2 Instances**:
  - Web Servers: In public subnets.
  - App Servers: In private subnets.
  - Databases: In private subnets.

#### 5. **Security and Best Practices**

1. **Least Privilege**:
   - Apply the principle of least privilege for security groups and IAM roles.
   
2. **Monitoring and Logging**:
   - Enable VPC Flow Logs to capture information about the IP traffic going to and from network interfaces.

3. **High Availability**:
   - Use multiple Availability Zones for your resources to ensure high availability.

4. **Regular Audits**:
   - Regularly audit security group rules, network ACLs, and IAM policies.

By following this detailed guide, you can set up a secure, scalable, and robust VPC architecture on AWS tailored to your application's needs.


Certainly! Below is a text-based visual representation of a VPC architecture for a sample web application:

```
+--------------------------+                                         +--------------------------+
|       Public Subnet 1    |                                         |       Public Subnet 2    |
|       (10.0.1.0/24)      |                                         |       (10.0.3.0/24)      |
|                          |                                         |                          |
|   +------------------+   |                                         |   +------------------+   |
|   |  Web Server 1    |   |                                         |   |  Web Server 2    |   |
|   |  (EC2 Instance)  |   |                                         |   |  (EC2 Instance)  |   |
|   +------------------+   |                                         |   +------------------+   |
|         |   |             |                                         |         |   |             |
|         |   +-------------+------------+                   +--------+---------+   |             |
|         |                  |            |                   |          |            |             |
|         |                  |            |                   |          |            |             |
|   +-----+------------------+------+     |                   |    +-----+------------+-----+      |
|   | Internet Gateway (IGW)        |     |                   |    |  NAT Gateway (NGW)      |      |
|   +-------------------------------+     |                   |    +-------------------------+      |
|                                        |                   |                                          |
+--------------------------+             |                   |                                          |
|       Private Subnet 1   |             |                   |       Private Subnet 2   |              |
|       (10.0.2.0/24)      |             |                   |       (10.0.4.0/24)      |              |
|                          |             |                   |                          |              |
|   +------------------+   |             |                   |   +------------------+   |              |
|   |  App Server 1    |   |             |                   |   |  App Server 2    |   |              |
|   |  (EC2 Instance)  |   |             |                   |   |  (EC2 Instance)  |   |              |
|   +------------------+   |             |                   |   +------------------+   |              |
|                          |             |                   |                          |              |
|   +------------------+   |             |                   |   +------------------+   |              |
|   |  DB Server 1     |   |             |                   |   |  DB Server 2     |   |              |
|   |  (EC2 Instance)  |   |             |                   |   |  (EC2 Instance)  |   |              |
|   +------------------+   |             |                   |   +------------------+   |              |
|                          |             |                   |                          |              |
+--------------------------+             |                   +--------------------------+              |
                                          |                                                                      |
                                          +--------------------------------------------------------------+
                                                                                       |
                                                                                       |
                                                                               +-------------------+
                                                                               |   Route Table     |
                                                                               |   (Public)        |
                                                                               |   +-------------+ |
                                                                               |   |  0.0.0.0/0  | |
                                                                               |   | -> IGW      | |
                                                                               |   +-------------+ |
                                                                               +-------------------+
                                                                                       |
                                                                                       |
                                                                               +-------------------+
                                                                               |   Route Table     |
                                                                               |   (Private)       |
                                                                               |   +-------------+ |
                                                                               |   |  0.0.0.0/0  | |
                                                                               |   | -> NGW      | |
                                                                               |   +-------------+ |
                                                                               +-------------------+
```

### Description:

- **Public Subnet 1 & 2**:
  - Contains Web Servers (EC2 instances) accessible from the internet.
  - Connected to an Internet Gateway (IGW) for internet access.

- **Private Subnet 1 & 2**:
  - Contains Application Servers and Database Servers (EC2 instances) not directly accessible from the internet.
  - Connected to a NAT Gateway (NGW) for outgoing internet access, such as updates and patches.

- **Internet Gateway (IGW)**:
  - Allows public subnets to communicate with the internet.

- **NAT Gateway (NGW)**:
  - Allows instances in the private subnets to connect to the internet without being directly accessible from the internet.

- **Route Tables**:
  - Public Route Table: Routes internet traffic (0.0.0.0/0) to the Internet Gateway.
  - Private Route Table: Routes internet traffic (0.0.0.0/0) to the NAT Gateway.

- **Security Groups (Not explicitly shown in diagram)**:
  - Web Security Group: Allows HTTP/HTTPS and SSH traffic.
  - App Security Group: Allows traffic from the Web Security Group.
  - DB Security Group: Allows traffic from the App Security Group.

This visual text diagram provides a simplified view of how a VPC can be structured to host a web application with multiple tiers (web, application, database), ensuring security and high availability by leveraging public and private subnets, route tables, and gateways.


Below are detailed Terraform scripts to set up a VPC for an e-commerce company aiming to host its online store on AWS with high availability, security, and scalability.

### 1. **Main Terraform Configuration File (main.tf)**

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "ecommerce-vpc"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-2"
  }
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "private-subnet-1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = "private-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "ecommerce-igw"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet_1.id
  tags = {
    Name = "ecommerce-nat"
  }
}

resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "public_subnet_1_rt_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet_2_rt_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "private_subnet_1_rt_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_subnet_2_rt_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.main.id

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

resource "aws_security_group" "app_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app-sg"
  }
}

resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "db-sg"
  }
}

resource "aws_instance" "web" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_subnet_1.id
  security_groups        = [aws_security_group.web_sg.name]
  associate_public_ip_address = true

  tags = {
    Name = "web-server"
  }
}

resource "aws_instance" "app" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private_subnet_1.id
  security_groups        = [aws_security_group.app_sg.name]

  tags = {
    Name = "app-server"
  }
}

resource "aws_instance" "db" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private_subnet_2.id
  security_groups        = [aws_security_group.db_sg.name]

  tags = {
    Name = "db-server"
  }
}
```

### 2. **Variables File (variables.tf)**

```hcl
variable "region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
}
```

### 3. **Outputs File (outputs.tf)**

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_1_id" {
  value = aws_subnet.public_subnet_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_subnet_2.id
}

output "private_subnet_1_id" {
  value = aws_subnet.private_subnet_1.id
}

output "private_subnet_2_id" {
  value = aws_subnet.private_subnet_2.id
}

output "internet_gateway_id" {
  value = aws_internet_gateway.igw.id
}

output "nat_gateway_id" {
  value = aws_nat_gateway.nat.id
}

output "web_instance_public_ip" {
  value = aws_instance.web.public_ip
}

output "app_instance_private_ip" {
  value = aws_instance.app.private_ip
}

output "db_instance_private_ip" {
  value = aws_instance.db.private_ip
}
```

### Steps to Deploy

1. **Initialize Terraform**:
   ```sh
   terraform init
   ```

2. **Plan the Deployment**:
   ```sh
   terraform plan
   ```

3. **Apply the Deployment**:
   ```sh
   terraform apply
   ```

This Terraform configuration sets up a highly available, secure, and scalable architecture for an e-commerce company on AWS. It includes public and private subnets spread across two availability zones, an internet gateway for public access, a NAT gateway for outbound access from private subnets, and security groups to control access between the web, application, and database servers. Adjust the AMI IDs, instance types, and other parameters as needed to fit your specific requirements.


Below are Terraform scripts for setting up a Hybrid Cloud Environment for a Financial Services company. This setup includes a VPC with public and private subnets, an Internet Gateway, a VPN Gateway for secure connections to the on-premises data center, and necessary route tables and security groups.

### 1. **Main Terraform Configuration File (main.tf)**

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "financial-services-vpc"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-2"
  }
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "private-subnet-1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = "private-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "financial-services-igw"
  }
}

resource "aws_vpn_gateway" "vpn_gw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "financial-services-vpn-gw"
  }
}

resource "aws_customer_gateway" "cg" {
  bgp_asn    = 65000
  ip_address = "203.0.113.12" # Replace with the actual public IP address of your on-premises VPN device
  type       = "ipsec.1"
  tags = {
    Name = "financial-services-cg"
  }
}

resource "aws_vpn_connection" "vpn" {
  customer_gateway_id = aws_customer_gateway.cg.id
  vpn_gateway_id      = aws_vpn_gateway.vpn_gw.id
  type                = "ipsec.1"
  static_routes_only  = true

  tags = {
    Name = "financial-services-vpn"
  }
}

resource "aws_vpn_connection_route" "route" {
  vpn_connection_id = aws_vpn_connection.vpn.id
  destination_cidr_block = "192.168.1.0/24" # Replace with the actual on-premises network CIDR block
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "192.168.1.0/24" # Replace with the actual on-premises network CIDR block
    gateway_id = aws_vpn_gateway.vpn_gw.id
  }
  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "public_subnet_1_rt_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet_2_rt_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "private_subnet_1_rt_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_subnet_2_rt_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.main.id

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

resource "aws_security_group" "app_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app-sg"
  }
}

resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "db-sg"
  }
}

resource "aws_instance" "web" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_subnet_1.id
  security_groups        = [aws_security_group.web_sg.name]
  associate_public_ip_address = true

  tags = {
    Name = "web-server"
  }
}

resource "aws_instance" "app" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private_subnet_1.id
  security_groups        = [aws_security_group.app_sg.name]

  tags = {
    Name = "app-server"
  }
}

resource "aws_instance" "db" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private_subnet_2.id
  security_groups        = [aws_security_group.db_sg.name]

  tags = {
    Name = "db-server"
  }
}
```

### 2. **Variables File (variables.tf)**

```hcl
variable "region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
}
```

### 3. **Outputs File (outputs.tf)**

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_1_id" {
  value = aws_subnet.public_subnet_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_subnet_2.id
}

output "private_subnet_1_id" {
  value = aws_subnet.private_subnet_1.id
}

output "private_subnet_2_id" {
  value = aws_subnet.private_subnet_2.id
}

output "internet_gateway_id" {
  value = aws_internet_gateway.igw.id
}

output "vpn_gateway_id" {
  value = aws_vpn_gateway.vpn_gw.id
}

output "vpn_connection_id" {
  value = aws_vpn_connection.vpn.id
}

output "web_instance_public_ip" {
  value = aws_instance.web.public_ip
}

output "app_instance_private_ip" {
  value =

 aws_instance.app.private_ip
}

output "db_instance_private_ip" {
  value = aws_instance.db.private_ip
}
```

### Steps to Deploy

1. **Initialize Terraform**:
   ```sh
   terraform init
   ```

2. **Plan the Deployment**:
   ```sh
   terraform plan
   ```

3. **Apply the Deployment**:
   ```sh
   terraform apply
   ```

This Terraform configuration sets up a Hybrid Cloud Environment for a financial services company, providing a secure and scalable architecture on AWS. It includes public and private subnets, an Internet Gateway for public access, a VPN Gateway for secure connections to the on-premises data center, and necessary route tables and security groups. Adjust the CIDR blocks, IP addresses, AMI IDs, instance types, and other parameters as needed to fit your specific requirements.


Below are Terraform scripts to set up a VPC for a media streaming company aiming to perform big data analytics on AWS. This setup includes a VPC with public and private subnets, an Internet Gateway, NAT Gateway, and necessary route tables and security groups. Additionally, it sets up an Amazon EMR cluster for big data processing.

### 1. **Main Terraform Configuration File (main.tf)**

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "media-streaming-vpc"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-2"
  }
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "private-subnet-1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = "private-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "media-streaming-igw"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet_1.id
  tags = {
    Name = "media-streaming-nat"
  }
}

resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "public_subnet_1_rt_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet_2_rt_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "private_subnet_1_rt_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_subnet_2_rt_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_security_group" "emr_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "emr-sg"
  }
}

resource "aws_emr_cluster" "emr" {
  name          = "media-streaming-emr-cluster"
  release_label = "emr-6.3.0"

  applications = [
    "Hadoop",
    "Spark"
  ]

  service_role = aws_iam_role.emr_service_role.name
  ec2_attributes {
    instance_profile = aws_iam_instance_profile.emr_instance_profile.name
    subnet_id        = aws_subnet.private_subnet_1.id
  }

  master_instance_group {
    instance_type = "m5.xlarge"
  }

  core_instance_group {
    instance_type = "m5.xlarge"
    instance_count = 2
  }

  tags = {
    Name = "media-streaming-emr-cluster"
  }

  visible_to_all_users = true
  termination_protection = false
}

resource "aws_iam_role" "emr_service_role" {
  name = "emr_service_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "emr_service_policy_attachment" {
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

resource "aws_iam_instance_profile" "emr_instance_profile" {
  name = "emr_instance_profile"
  role = aws_iam_role.emr_instance_role.name
}

resource "aws_iam_role" "emr_instance_role" {
  name = "emr_instance_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "emr_instance_policy_attachment" {
  role       = aws_iam_role.emr_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}
```

### 2. **Variables File (variables.tf)**

```hcl
variable "region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
}
```

### 3. **Outputs File (outputs.tf)**

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_1_id" {
  value = aws_subnet.public_subnet_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_subnet_2.id
}

output "private_subnet_1_id" {
  value = aws_subnet.private_subnet_1.id
}

output "private_subnet_2_id" {
  value = aws_subnet.private_subnet_2.id
}

output "internet_gateway_id" {
  value = aws_internet_gateway.igw.id
}

output "nat_gateway_id" {
  value = aws_nat_gateway.nat.id
}

output "emr_cluster_id" {
  value = aws_emr_cluster.emr.id
}
```

### Steps to Deploy

1. **Initialize Terraform**:
   ```sh
   terraform init
   ```

2. **Plan the Deployment**:
   ```sh
   terraform plan
   ```

3. **Apply the Deployment**:
   ```sh
   terraform apply
   ```

This Terraform configuration sets up a secure and scalable architecture for a media streaming company's big data analytics on AWS. It includes public and private subnets, an Internet Gateway, a NAT Gateway, and an Amazon EMR cluster for big data processing. Adjust the CIDR blocks, instance types, AMI IDs, and other parameters as needed to fit your specific requirements.


Below are Terraform scripts to set up a VPC for a media streaming company aiming to perform big data analytics on AWS. This setup includes a VPC with public and private subnets, an Internet Gateway, NAT Gateway, and necessary route tables and security groups. Additionally, it sets up an Amazon EMR cluster for big data processing.

### 1. **Main Terraform Configuration File (main.tf)**

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "media-streaming-vpc"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-2"
  }
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "private-subnet-1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = "private-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "media-streaming-igw"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet_1.id
  tags = {
    Name = "media-streaming-nat"
  }
}

resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "public_subnet_1_rt_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet_2_rt_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "private_subnet_1_rt_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_subnet_2_rt_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_security_group" "emr_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "emr-sg"
  }
}

resource "aws_emr_cluster" "emr" {
  name          = "media-streaming-emr-cluster"
  release_label = "emr-6.3.0"

  applications = [
    "Hadoop",
    "Spark"
  ]

  service_role = aws_iam_role.emr_service_role.name
  ec2_attributes {
    instance_profile = aws_iam_instance_profile.emr_instance_profile.name
    subnet_id        = aws_subnet.private_subnet_1.id
  }

  master_instance_group {
    instance_type = "m5.xlarge"
  }

  core_instance_group {
    instance_type = "m5.xlarge"
    instance_count = 2
  }

  tags = {
    Name = "media-streaming-emr-cluster"
  }

  visible_to_all_users = true
  termination_protection = false
}

resource "aws_iam_role" "emr_service_role" {
  name = "emr_service_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "emr_service_policy_attachment" {
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

resource "aws_iam_instance_profile" "emr_instance_profile" {
  name = "emr_instance_profile"
  role = aws_iam_role.emr_instance_role.name
}

resource "aws_iam_role" "emr_instance_role" {
  name = "emr_instance_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "emr_instance_policy_attachment" {
  role       = aws_iam_role.emr_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}
```

### 2. **Variables File (variables.tf)**

```hcl
variable "region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
}
```

### 3. **Outputs File (outputs.tf)**

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_1_id" {
  value = aws_subnet.public_subnet_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_subnet_2.id
}

output "private_subnet_1_id" {
  value = aws_subnet.private_subnet_1.id
}

output "private_subnet_2_id" {
  value = aws_subnet.private_subnet_2.id
}

output "internet_gateway_id" {
  value = aws_internet_gateway.igw.id
}

output "nat_gateway_id" {
  value = aws_nat_gateway.nat.id
}

output "emr_cluster_id" {
  value = aws_emr_cluster.emr.id
}
```

### Steps to Deploy

1. **Initialize Terraform**:
   ```sh
   terraform init
   ```

2. **Plan the Deployment**:
   ```sh
   terraform plan
   ```

3. **Apply the Deployment**:
   ```sh
   terraform apply
   ```

This Terraform configuration sets up a secure and scalable architecture for a media streaming company's big data analytics on AWS. It includes public and private subnets, an Internet Gateway, a NAT Gateway, and an Amazon EMR cluster for big data processing. Adjust the CIDR blocks, instance types, AMI IDs, and other parameters as needed to fit your specific requirements.
