### Detailed Guide on AWS VPN

AWS VPN (Virtual Private Network) allows secure connections between on-premises networks, remote offices, client devices, and AWS resources. There are two main types of AWS VPN: Site-to-Site VPN and Client VPN.

#### **1. Site-to-Site VPN**
Site-to-Site VPN connects your on-premises or remote networks to AWS VPCs securely. It provides two tunnels for redundancy and automatic failover.

##### **Setup Process**

**Step 1: Create a Virtual Private Gateway (VGW)**
- Navigate to the VPC Dashboard in the AWS Management Console.
- Select "Virtual Private Gateways" from the left-hand menu.
- Click "Create Virtual Private Gateway."
- Provide a name and select the ASN (Autonomous System Number). Click "Create."

**Step 2: Attach the VGW to a VPC**
- Select the newly created VGW.
- Click "Actions" and then "Attach to VPC."
- Choose the VPC and click "Attach."

**Step 3: Create a Customer Gateway**
- Select "Customer Gateways" from the left-hand menu.
- Click "Create Customer Gateway."
- Provide a name, the static IP address of your on-premises router, and the BGP ASN if needed. Click "Create."

**Step 4: Create a Site-to-Site VPN Connection**
- Select "Site-to-Site VPN Connections" from the left-hand menu.
- Click "Create VPN Connection."
- Provide a name, select the VGW and Customer Gateway created earlier.
- Choose the routing type (Static or Dynamic). For Static, enter the routes manually. For Dynamic, use BGP.
- Click "Create VPN Connection."

**Step 5: Download Configuration**
- Select the VPN connection.
- Click "Download Configuration" to get the VPN configuration for your on-premises device. This file will contain the necessary parameters for configuring your on-premises router.

**Step 6: Configure Your On-Premises Router**
- Use the downloaded configuration file to configure your on-premises router. Follow the vendor-specific instructions for your router.

**Step 7: Update Route Tables**
- Update your VPC route tables to route traffic through the VPN connection. Add routes pointing to your on-premises network via the VGW.

##### **Monitoring and Maintenance**
- Regularly monitor the VPN connection health using CloudWatch.
- Configure CloudWatch alarms to notify you of any connection issues.

#### **2. Client VPN**
Client VPN enables secure connections from client devices to your AWS resources or on-premises network.

##### **Setup Process**

**Step 1: Create a Client VPN Endpoint**
- Navigate to the VPC Dashboard in the AWS Management Console.
- Select "Client VPN Endpoints" from the left-hand menu.
- Click "Create Client VPN Endpoint."
- Provide the necessary details:
  - Client CIDR range (range of IP addresses to assign to VPN clients).
  - Server certificate ARN.
  - Authentication options (Active Directory, mutual authentication, etc.).
  - Connection logging options.

**Step 2: Associate a Target Network**
- Select the newly created Client VPN endpoint.
- Click "Associations" and then "Associate."
- Select the VPC and subnet to associate with the VPN endpoint. Click "Associate."

**Step 3: Authorize Ingress Traffic**
- Select the Client VPN endpoint.
- Click "Authorization rules."
- Add authorization rules to allow client IP addresses to access specific resources.

**Step 4: Download and Configure Client Configuration**
- Download the client configuration file from the Client VPN endpoint details.
- Distribute the configuration file to your VPN clients.
- Use OpenVPN client or AWS-provided VPN client software to connect to the VPN.

**Step 5: Configure Route Tables**
- Update the VPC route tables to allow traffic from the VPN endpoint to your resources.
- Add routes pointing to the client CIDR range via the associated subnet.

##### **Monitoring and Maintenance**
- Monitor the Client VPN connections using CloudWatch.
- Configure CloudWatch alarms for connection issues and usage metrics.

### **Best Practices**
- **Security:** Always use strong authentication and encryption methods. Regularly rotate keys and certificates.
- **High Availability:** Utilize the dual-tunnel setup for Site-to-Site VPN for redundancy. Consider using AWS Direct Connect for critical applications.
- **Performance:** Monitor VPN performance metrics and scale the infrastructure as needed.
- **Logging:** Enable logging for both Site-to-Site and Client VPNs to track usage and troubleshoot issues.

### **Cost Considerations**
- **Site-to-Site VPN:** Charged per VPN connection-hour and per GB of data transferred.
- **Client VPN:** Charged per active client connection-hour.

### **Conclusion**
AWS VPN services provide secure and scalable solutions for connecting your on-premises networks and remote clients to AWS. Proper setup, monitoring, and maintenance are key to ensuring reliable and secure VPN connections.


### Real-World Examples of AWS VPN

#### **Example 1: Enterprise HQ and Branch Office Connectivity**

**Scenario:**
A large enterprise with a headquarters (HQ) and multiple branch offices needs to connect all its offices to its AWS VPC for centralized data storage and application hosting.

**Solution:**

1. **Site-to-Site VPN Setup for HQ:**
   - Create a Virtual Private Gateway (VGW) and attach it to the main VPC in AWS.
   - Create a Customer Gateway for the HQ with the public IP of the HQ’s on-premises router.
   - Establish a Site-to-Site VPN connection between the HQ and the AWS VPC, using BGP for dynamic routing to handle multiple subnets.

2. **Site-to-Site VPN Setup for Branch Offices:**
   - For each branch office, create a Customer Gateway with the public IP of the branch office’s router.
   - Establish separate Site-to-Site VPN connections from each branch office to the AWS VPC.
   - Use static routing if the branch offices have simple network configurations; otherwise, use BGP.

3. **Configuration and Routing:**
   - Configure the on-premises routers at the HQ and branch offices with the VPN configurations provided by AWS.
   - Update VPC route tables to route traffic from the branch office networks through the VGW.

**Benefits:**
- Centralized data access and application hosting.
- Secure and encrypted communication channels.
- Simplified network management with AWS’s built-in monitoring and alerting.

#### **Example 2: Remote Workforce Access**

**Scenario:**
A company has a large remote workforce that needs secure access to internal applications and resources hosted on AWS.

**Solution:**

1. **Client VPN Endpoint Setup:**
   - Create a Client VPN endpoint in AWS.
   - Configure the VPN endpoint with the necessary authentication method (e.g., Active Directory, mutual authentication using certificates).
   - Associate the Client VPN endpoint with the appropriate VPC subnets to provide access to resources.

2. **Client Configuration:**
   - Download the client configuration file and distribute it to remote employees.
   - Employees use OpenVPN or AWS VPN client software to connect to the Client VPN endpoint.

3. **Access and Security Management:**
   - Define authorization rules to specify which network resources remote clients can access.
   - Update VPC route tables to allow traffic from the client CIDR range to the necessary resources.
   - Enable logging and monitoring to track VPN usage and detect potential security issues.

**Benefits:**
- Secure remote access for employees from any location.
- Scalable solution that can accommodate a growing remote workforce.
- Simplified user management and access control through integration with existing authentication systems.

#### **Example 3: E-commerce Company Hosting Online Store on AWS**

**Scenario:**
An e-commerce company wants to host its online store on AWS with high availability, security, and scalability while maintaining secure connections to its on-premises data center.

**Solution:**

1. **Site-to-Site VPN Setup:**
   - Create a Virtual Private Gateway (VGW) and attach it to the VPC hosting the online store.
   - Create a Customer Gateway for the company’s on-premises data center.
   - Establish a Site-to-Site VPN connection between the data center and AWS VPC for secure data exchange.

2. **AWS Infrastructure:**
   - Set up multiple Availability Zones (AZs) for high availability.
   - Use Auto Scaling and Elastic Load Balancing (ELB) for scalability and redundancy.
   - Implement security groups and Network ACLs to control inbound and outbound traffic.

3. **Database Connectivity:**
   - Deploy Amazon RDS for database hosting with Multi-AZ deployment for high availability.
   - Use the Site-to-Site VPN to securely connect the on-premises data center with the RDS instances.

4. **Monitoring and Security:**
   - Enable AWS CloudTrail and AWS Config for monitoring and compliance.
   - Use AWS WAF and AWS Shield for protection against web attacks.
   - Implement IAM roles and policies for access management.

**Terraform Script for VPN Setup:**
```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_vpn_gateway" "vgw" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_customer_gateway" "cgw" {
  bgp_asn    = 65000
  ip_address = "198.51.100.0"  # Replace with your on-premises public IP
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "vpn_connection" {
  customer_gateway_id = aws_customer_gateway.cgw.id
  vpn_gateway_id      = aws_vpn_gateway.vgw.id
  type                = "ipsec.1"

  static_routes_only = true

  tags = {
    Name = "example-vpn-connection"
  }
}

resource "aws_vpn_connection_route" "vpn_route" {
  vpn_connection_id = aws_vpn_connection.vpn_connection.id
  destination_cidr_block = "192.168.1.0/24"  # Replace with your on-premises subnet
}

resource "aws_route" "vpn_route" {
  route_table_id         = aws_vpc.main_vpc.main_route_table_id
  destination_cidr_block = "192.168.1.0/24"  # Replace with your on-premises subnet
  gateway_id             = aws_vpn_gateway.vgw.id
}
```

**Benefits:**
- High availability and scalability of the online store.
- Secure data transmission between the on-premises data center and AWS.
- Robust security measures to protect against threats and attacks.

These examples demonstrate how AWS VPN can be leveraged to address various business needs, ensuring secure, reliable, and scalable network connections.


Sure! Below are the Terraform scripts for each of the real-world examples.

### **Example 1: Enterprise HQ and Branch Office Connectivity**

#### **Terraform Script for HQ Site-to-Site VPN Setup**

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_vpn_gateway" "vgw" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_customer_gateway" "cgw_hq" {
  bgp_asn    = 65000
  ip_address = "198.51.100.1"  # Replace with HQ on-premises public IP
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "vpn_hq" {
  customer_gateway_id = aws_customer_gateway.cgw_hq.id
  vpn_gateway_id      = aws_vpn_gateway.vgw.id
  type                = "ipsec.1"

  static_routes_only = true

  tags = {
    Name = "hq-vpn-connection"
  }
}

resource "aws_vpn_connection_route" "vpn_route_hq" {
  vpn_connection_id      = aws_vpn_connection.vpn_hq.id
  destination_cidr_block = "192.168.1.0/24"  # Replace with HQ on-premises subnet
}

resource "aws_route" "vpn_route_hq" {
  route_table_id         = aws_vpc.main_vpc.main_route_table_id
  destination_cidr_block = "192.168.1.0/24"  # Replace with HQ on-premises subnet
  gateway_id             = aws_vpn_gateway.vgw.id
}
```

#### **Terraform Script for Branch Office Site-to-Site VPN Setup**

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_customer_gateway" "cgw_branch" {
  bgp_asn    = 65000
  ip_address = "198.51.100.2"  # Replace with Branch Office on-premises public IP
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "vpn_branch" {
  customer_gateway_id = aws_customer_gateway.cgw_branch.id
  vpn_gateway_id      = aws_vpn_gateway.vgw.id
  type                = "ipsec.1"

  static_routes_only = true

  tags = {
    Name = "branch-vpn-connection"
  }
}

resource "aws_vpn_connection_route" "vpn_route_branch" {
  vpn_connection_id      = aws_vpn_connection.vpn_branch.id
  destination_cidr_block = "192.168.2.0/24"  # Replace with Branch Office on-premises subnet
}

resource "aws_route" "vpn_route_branch" {
  route_table_id         = aws_vpc.main_vpc.main_route_table_id
  destination_cidr_block = "192.168.2.0/24"  # Replace with Branch Office on-premises subnet
  gateway_id             = aws_vpn_gateway.vgw.id
}
```

### **Example 2: Remote Workforce Access**

#### **Terraform Script for Client VPN Endpoint Setup**

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "vpn_subnet" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_security_group" "vpn_sg" {
  vpc_id = aws_vpc.main_vpc.id

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
}

resource "aws_client_vpn_endpoint" "client_vpn" {
  description               = "Client VPN Endpoint"
  server_certificate_arn    = "arn:aws:acm:us-west-2:123456789012:certificate/abcd1234-efgh-5678-ijkl-9012mnopqrst"  # Replace with your ACM certificate ARN
  authentication_options {
    type                       = "certificate-authentication"
    root_certificate_chain_arn = "arn:aws:acm:us-west-2:123456789012:certificate/abcd1234-efgh-5678-ijkl-9012mnopqrst"  # Replace with your ACM certificate ARN
  }
  connection_log_options {
    enabled             = true
    cloudwatch_log_group = "client-vpn-logs"
    cloudwatch_log_stream = "client-vpn-log-stream"
  }
  dns_servers            = ["8.8.8.8"]
  client_cidr_block      = "10.2.0.0/16"
  split_tunnel           = false
  security_group_ids     = [aws_security_group.vpn_sg.id]
  vpc_id                 = aws_vpc.main_vpc.id
  transport_protocol     = "udp"
}

resource "aws_client_vpn_network_association" "vpn_association" {
  client_vpn_endpoint_id = aws_client_vpn_endpoint.client_vpn.id
  subnet_id              = aws_subnet.vpn_subnet.id
}

resource "aws_client_vpn_authorization_rule" "vpn_auth_rule" {
  client_vpn_endpoint_id = aws_client_vpn_endpoint.client_vpn.id
  target_network_cidr    = "10.0.0.0/16"
  authorize_all_groups   = true
}
```

### **Example 3: E-commerce Company Hosting Online Store on AWS**

#### **Terraform Script for Site-to-Site VPN Setup**

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "ecommerce_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_vpn_gateway" "vgw" {
  vpc_id = aws_vpc.ecommerce_vpc.id
}

resource "aws_customer_gateway" "cgw" {
  bgp_asn    = 65000
  ip_address = "198.51.100.3"  # Replace with e-commerce company on-premises public IP
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "vpn_connection" {
  customer_gateway_id = aws_customer_gateway.cgw.id
  vpn_gateway_id      = aws_vpn_gateway.vgw.id
  type                = "ipsec.1"

  static_routes_only = true

  tags = {
    Name = "ecommerce-vpn-connection"
  }
}

resource "aws_vpn_connection_route" "vpn_route" {
  vpn_connection_id      = aws_vpn_connection.vpn_connection.id
  destination_cidr_block = "192.168.3.0/24"  # Replace with e-commerce company on-premises subnet
}

resource "aws_route" "vpn_route" {
  route_table_id         = aws_vpc.ecommerce_vpc.main_route_table_id
  destination_cidr_block = "192.168.3.0/24"  # Replace with e-commerce company on-premises subnet
  gateway_id             = aws_vpn_gateway.vgw.id
}
```

These Terraform scripts provide a starting point for configuring AWS VPN connections in various scenarios. Adjust the configurations as necessary to fit specific requirements, such as IP addresses, subnet CIDR blocks, and authentication methods.


### Detailed Guide for AWS Direct Connect

AWS Direct Connect is a dedicated network connection that allows you to establish a direct link between your on-premises data centers and AWS. This dedicated connection can provide lower latency, higher bandwidth, and more consistent network performance compared to internet-based connections.

#### **1. Benefits of AWS Direct Connect**
- **Lower Latency and Higher Bandwidth:** Dedicated connection can reduce latency and provide higher bandwidth compared to internet connections.
- **Consistent Network Performance:** With a dedicated line, you avoid internet congestion, ensuring more reliable performance.
- **Cost-Effective:** Potentially lower data transfer costs compared to data transfer over the public internet.
- **Private Connectivity:** Enhances security by avoiding the public internet.

#### **2. Components of AWS Direct Connect**
- **Direct Connect Locations:** Physical locations where AWS Direct Connect connections are available.
- **Direct Connect Gateway:** Allows you to connect your AWS Direct Connect connection to one or more VPCs in different regions.
- **Virtual Interfaces (VIF):** Logical interfaces to connect to AWS resources, either public or private.

#### **3. Setup Process**

**Step 1: Choose a Direct Connect Location**
- Identify the AWS Direct Connect location that is closest to your on-premises data center. AWS provides a list of available Direct Connect locations.

**Step 2: Create a Connection**
- Go to the AWS Direct Connect console.
- Click "Create Connection."
- Provide a name for the connection, select the desired AWS Direct Connect location, choose the port speed, and click "Create Connection."

**Step 3: Download the Letter of Authorization (LOA)**
- After creating the connection, AWS will provide a Letter of Authorization and Connecting Facility Assignment (LOA-CFA).
- Provide this document to your network provider or colocation provider to establish the physical connection to the AWS Direct Connect location.

**Step 4: Configure the On-Premises Router**
- Configure your on-premises router to connect to the AWS Direct Connect location. You will need to work with your network provider to ensure proper configuration.
- AWS provides router configuration details which include IP addresses, VLAN IDs, and other necessary settings.

**Step 5: Create a Virtual Interface**
- In the AWS Direct Connect console, navigate to "Virtual Interfaces."
- Click "Create Virtual Interface."
  - **Public VIF:** Connects to AWS public services (like S3, EC2).
  - **Private VIF:** Connects to your VPC.
- Provide the necessary details such as connection ID, VLAN ID, and BGP settings.

**Step 6: Configure the Virtual Interface**
- Configure BGP on your on-premises router with the provided BGP ASN and IP addresses.
- Establish the BGP peering session between your router and AWS.

**Step 7: Verify the Connection**
- Check the AWS Direct Connect console to verify that the connection and virtual interfaces are up and running.
- Monitor the BGP session status and ensure that routes are being advertised and received correctly.

#### **4. Setting Up Direct Connect Gateway**
To connect multiple VPCs across different regions to your Direct Connect connection, use a Direct Connect Gateway.

**Step 1: Create a Direct Connect Gateway**
- Go to the AWS Direct Connect console.
- Click "Create Direct Connect Gateway."
- Provide a name and an ASN for the gateway and click "Create Direct Connect Gateway."

**Step 2: Associate the Direct Connect Gateway with Virtual Interfaces**
- Select the Direct Connect Gateway.
- Click "Associate Virtual Interface."
- Choose the Virtual Interface you created earlier.

**Step 3: Associate the Direct Connect Gateway with VPCs**
- In the Direct Connect console, navigate to "Virtual Private Gateways."
- Select the VGW associated with your VPC.
- Click "Actions" and then "Associate with Direct Connect Gateway."
- Choose the Direct Connect Gateway and complete the association.

#### **5. Monitoring and Maintenance**
- Use AWS CloudWatch to monitor Direct Connect metrics such as connection state, data transfer rates, and BGP sessions.
- Set up CloudWatch alarms to notify you of any connection issues or performance degradation.
- Regularly review and update BGP configurations as needed.

### Example Terraform Script for AWS Direct Connect

Here is a simple example to create a Direct Connect connection and virtual interface using Terraform:

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_dx_connection" "example" {
  name             = "example-connection"
  bandwidth        = "1Gbps"
  location         = "EqDC2"  # Replace with your chosen Direct Connect location
}

resource "aws_dx_gateway" "example" {
  name = "example-dx-gateway"
  amazon_side_asn = "64512"
}

resource "aws_dx_private_virtual_interface" "example" {
  connection_id = aws_dx_connection.example.id
  vlan          = 4094
  address_family = "ipv4"
  bgp_asn       = 65000

  dx_gateway_id = aws_dx_gateway.example.id

  tags = {
    Name = "example-private-vif"
  }
}
```

#### **Cost Considerations**
- **Port Hour Fees:** Based on the port speed and duration.
- **Data Transfer Fees:** Based on the amount of data transferred through the connection.

### Conclusion

AWS Direct Connect provides a reliable, high-performance, and secure way to connect your on-premises network to AWS. By following the setup process and best practices, you can ensure a robust and efficient network connection for your workloads.


Certainly! Here are some real-world examples of AWS Direct Connect setups using Terraform, tailored to different use cases.

### Example 1: Hybrid Cloud Architecture

**Scenario:**
A large enterprise has an on-premises data center and wants to extend its infrastructure to AWS for hybrid cloud capabilities. They need low-latency and high-bandwidth connections between their on-premises data center and AWS VPC.

#### **Terraform Script for Hybrid Cloud Architecture**

```hcl
provider "aws" {
  region = "us-west-2"
}

# Direct Connect Connection
resource "aws_dx_connection" "hybrid_connection" {
  name       = "hybrid-cloud-connection"
  bandwidth  = "1Gbps"
  location   = "EqDC2"  # Replace with your chosen Direct Connect location
}

# Direct Connect Gateway
resource "aws_dx_gateway" "hybrid_dx_gateway" {
  name          = "hybrid-dx-gateway"
  amazon_side_asn = "64512"
}

# Virtual Private Gateway
resource "aws_vpn_gateway" "vgw" {
  vpc_id = aws_vpc.main_vpc.id
}

# VPC
resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

# Private Virtual Interface
resource "aws_dx_private_virtual_interface" "hybrid_private_vif" {
  connection_id = aws_dx_connection.hybrid_connection.id
  vlan          = 4094
  address_family = "ipv4"
  bgp_asn       = 65000

  dx_gateway_id = aws_dx_gateway.hybrid_dx_gateway.id

  tags = {
    Name = "hybrid-private-vif"
  }
}

# Associate Direct Connect Gateway with Virtual Private Gateway
resource "aws_vpn_gateway_attachment" "vgw_attachment" {
  vpc_id     = aws_vpc.main_vpc.id
  vpn_gateway_id = aws_vpn_gateway.vgw.id
}

resource "aws_dx_gateway_association" "hybrid_dx_gateway_assoc" {
  dx_gateway_id        = aws_dx_gateway.hybrid_dx_gateway.id
  vpn_gateway_id       = aws_vpn_gateway.vgw.id
  allowed_prefixes = ["10.0.0.0/16"]
}
```

### Example 2: Multi-Region VPC Connectivity

**Scenario:**
A company has multiple VPCs in different regions and needs to establish low-latency, high-bandwidth connections between them and the on-premises data center using AWS Direct Connect.

#### **Terraform Script for Multi-Region VPC Connectivity**

```hcl
provider "aws" {
  region = "us-west-2"
}

# Direct Connect Connection
resource "aws_dx_connection" "multi_region_connection" {
  name       = "multi-region-connection"
  bandwidth  = "1Gbps"
  location   = "EqDC2"  # Replace with your chosen Direct Connect location
}

# Direct Connect Gateway
resource "aws_dx_gateway" "multi_region_dx_gateway" {
  name          = "multi-region-dx-gateway"
  amazon_side_asn = "64512"
}

# VPC in us-west-2
resource "aws_vpc" "us_west_vpc" {
  cidr_block = "10.0.0.0/16"
}

# VPC in us-east-1
provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

resource "aws_vpc" "us_east_vpc" {
  provider   = aws.us-east-1
  cidr_block = "10.1.0.0/16"
}

# Private Virtual Interface
resource "aws_dx_private_virtual_interface" "multi_region_private_vif" {
  connection_id = aws_dx_connection.multi_region_connection.id
  vlan          = 4094
  address_family = "ipv4"
  bgp_asn       = 65000

  dx_gateway_id = aws_dx_gateway.multi_region_dx_gateway.id

  tags = {
    Name = "multi-region-private-vif"
  }
}

# Virtual Private Gateway for us-west-2 VPC
resource "aws_vpn_gateway" "us_west_vgw" {
  vpc_id = aws_vpc.us_west_vpc.id
}

# Virtual Private Gateway for us-east-1 VPC
resource "aws_vpn_gateway" "us_east_vgw" {
  provider  = aws.us-east-1
  vpc_id    = aws_vpc.us_east_vpc.id
}

# Attach VPN Gateways
resource "aws_vpn_gateway_attachment" "us_west_vgw_attachment" {
  vpc_id        = aws_vpc.us_west_vpc.id
  vpn_gateway_id = aws_vpn_gateway.us_west_vgw.id
}

resource "aws_vpn_gateway_attachment" "us_east_vgw_attachment" {
  provider      = aws.us-east-1
  vpc_id        = aws_vpc.us_east_vpc.id
  vpn_gateway_id = aws_vpn_gateway.us_east_vgw.id
}

# Associate Direct Connect Gateway with Virtual Private Gateways
resource "aws_dx_gateway_association" "multi_region_dx_gateway_us_west_assoc" {
  dx_gateway_id        = aws_dx_gateway.multi_region_dx_gateway.id
  vpn_gateway_id       = aws_vpn_gateway.us_west_vgw.id
  allowed_prefixes = ["10.0.0.0/16"]
}

resource "aws_dx_gateway_association" "multi_region_dx_gateway_us_east_assoc" {
  dx_gateway_id        = aws_dx_gateway.multi_region_dx_gateway.id
  vpn_gateway_id       = aws_vpn_gateway.us_east_vgw.id
  allowed_prefixes = ["10.1.0.0/16"]
}
```

### Example 3: E-Commerce Company Hosting Online Store with Secure Backend Connectivity

**Scenario:**
An e-commerce company hosts its online store on AWS and requires secure and reliable backend connectivity to its on-premises data center for database replication and backend services.

#### **Terraform Script for E-Commerce Company**

```hcl
provider "aws" {
  region = "us-west-2"
}

# VPC
resource "aws_vpc" "ecommerce_vpc" {
  cidr_block = "10.0.0.0/16"
}

# Subnets
resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.ecommerce_vpc.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.ecommerce_vpc.id
  cidr_block = "10.0.2.0/24"
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.ecommerce_vpc.id
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.ecommerce_vpc.id
}

resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Route
resource "aws_route" "igw_route" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Direct Connect Connection
resource "aws_dx_connection" "ecommerce_connection" {
  name       = "ecommerce-connection"
  bandwidth  = "1Gbps"
  location   = "EqDC2"  # Replace with your chosen Direct Connect location
}

# Direct Connect Gateway
resource "aws_dx_gateway" "ecommerce_dx_gateway" {
  name          = "ecommerce-dx-gateway"
  amazon_side_asn = "64512"
}

# Private Virtual Interface
resource "aws_dx_private_virtual_interface" "ecommerce_private_vif" {
  connection_id = aws_dx_connection.ecommerce_connection.id
  vlan          = 4094
  address_family = "ipv4"
  bgp_asn       = 65000

  dx_gateway_id = aws_dx_gateway.ecommerce_dx_gateway.id

  tags = {
    Name = "ecommerce-private-vif"
  }
}

# Virtual Private Gateway
resource "aws_vpn_gateway" "ecommerce_vgw" {
  vpc_id = aws_vpc.ecommerce_vpc.id
}

# Attach Virtual Private Gateway
resource "aws_vpn_gateway_attachment" "ecommerce_vgw_attachment" {
  vpc_id        = aws_vpc.ecommerce_vpc.id
  vpn_gateway_id = aws_vpn_gateway.ecommerce_vgw.id
}

# Associate Direct Connect Gateway with Virtual Private Gateway
resource "aws_dx_gateway_association" "ecommerce_dx_gateway_assoc" {
  dx_gateway_id        = aws_dx_gateway.ecommerce_dx_gateway.id
  vpn_gateway_id       = aws_vpn_gateway.ecommerce_vgw.id
  allowed_prefixes = ["10.0.0.0/16"]
}
```

These Terraform scripts illustrate how to set up AWS Direct Connect for various real-world scenarios. Adjust the configurations and resource values to match your specific requirements and infrastructure setup.
