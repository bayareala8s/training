Azure Networking Fundamentals encompass a range of concepts and services that are essential for designing, deploying, and managing network solutions in Microsoft Azure. Here's an in-depth explanation of the core components and concepts:

### 1. **Virtual Networks (VNets)**
VNets are the foundation of Azure networking. They enable Azure resources to communicate securely with each other, the internet, and on-premises networks. Key aspects include:
- **Address Space:** Define the IP address range using CIDR notation.
- **Subnets:** Divide the VNet address space into multiple subnets to segment the network.
- **Network Security Groups (NSGs):** Control inbound and outbound traffic to subnets or individual VMs by defining security rules.
- **Service Endpoints:** Allow Azure services to be accessed securely from a VNet.

### 2. **Azure Virtual Private Network (VPN)**
Azure VPNs connect on-premises networks to Azure VNets through a secure and encrypted tunnel. There are two main types:
- **Point-to-Site VPN:** Connects individual clients to the Azure VNet.
- **Site-to-Site VPN:** Connects entire on-premises networks to Azure VNets.

### 3. **Azure ExpressRoute**
ExpressRoute provides a dedicated private connection between your on-premises network and Azure data centers. This connection doesn't go over the public internet, offering greater reliability, faster speeds, and lower latencies.

### 4. **Azure Load Balancer**
Load Balancer distributes incoming network traffic across multiple Azure resources to ensure high availability and reliability. Types include:
- **Public Load Balancer:** Routes traffic from the internet to VMs.
- **Internal Load Balancer:** Routes traffic within the Azure VNet.

### 5. **Azure Application Gateway**
Application Gateway is a web traffic load balancer that enables you to manage traffic to your web applications. It operates at the application layer (OSI Layer 7) and provides advanced routing, SSL termination, and Web Application Firewall (WAF) capabilities.

### 6. **Azure Traffic Manager**
Traffic Manager is a DNS-based traffic load balancer that distributes traffic across global Azure regions. It improves availability and responsiveness by directing traffic to the most appropriate endpoint based on routing methods like performance, priority, and geographic.

### 7. **Azure DNS**
Azure DNS hosts your DNS domains and provides name resolution using Microsoft’s Azure infrastructure. This service allows you to manage DNS records and ensure high availability and performance.

### 8. **Network Security**
Security is a critical aspect of Azure networking, involving various tools and practices:
- **Azure Firewall:** A managed, cloud-based network security service that protects your Azure Virtual Network resources.
- **DDoS Protection:** Azure DDoS Protection protects against distributed denial of service attacks.
- **NSGs and ASGs (Application Security Groups):** Provide security at a network and application level.

### 9. **Peering**
VNet Peering connects VNets to each other, allowing resources in different VNets to communicate. Peering can be within the same region or across regions (Global VNet Peering).

### 10. **Network Monitoring and Diagnostics**
Azure offers various tools to monitor and diagnose network issues:
- **Network Watcher:** Provides network monitoring, diagnostic, and visualization tools.
- **Azure Monitor:** Collects, analyzes, and acts on telemetry data from your Azure resources.

### Practical Example: Setting Up a Basic Azure Network

1. **Create a Virtual Network:**
   - Define the address space (e.g., 10.0.0.0/16).
   - Create subnets (e.g., front-end 10.0.1.0/24, back-end 10.0.2.0/24).

2. **Add Network Security Groups:**
   - Create NSGs and associate them with the subnets.
   - Define inbound and outbound security rules (e.g., allow HTTP/HTTPS traffic to the front-end subnet).

3. **Configure a VPN Gateway:**
   - Set up a VPN gateway for site-to-site VPN connectivity.
   - Configure the on-premises VPN device to establish the VPN connection.

4. **Deploy Load Balancer:**
   - Create a public load balancer.
   - Add backend pools, health probes, and load balancing rules to distribute traffic to VMs.

5. **Set Up Application Gateway:**
   - Deploy an application gateway with WAF.
   - Configure HTTP settings, listeners, and routing rules to manage web traffic.

By understanding and implementing these Azure networking fundamentals, you can build robust, secure, and scalable network solutions in Microsoft Azure.


### Real-World Examples of Azure Networking Implementations

#### 1. **E-Commerce Platform: High Availability and Scalability**
**Scenario:**
An e-commerce company wants to ensure its platform is highly available, scalable, and secure. They need to handle fluctuating traffic volumes, especially during peak shopping seasons.

**Solution:**
1. **Virtual Network (VNet):**
   - Create a VNet with multiple subnets (e.g., web, application, database).
   - Implement Network Security Groups (NSGs) to control traffic flow between subnets.

2. **Load Balancer:**
   - Use Azure Public Load Balancer to distribute incoming web traffic across multiple virtual machines (VMs) in the web subnet.
   - Set up health probes to monitor the health of VMs and automatically remove unhealthy instances from the load balancer pool.

3. **Application Gateway:**
   - Deploy Azure Application Gateway with Web Application Firewall (WAF) to protect against web exploits and common vulnerabilities.
   - Configure URL-based routing to direct user requests to specific VMs based on the URL path (e.g., product pages, checkout).

4. **Auto-Scaling:**
   - Implement Azure Virtual Machine Scale Sets (VMSS) to automatically scale the number of VMs based on traffic load, ensuring high availability and performance during peak times.

5. **ExpressRoute:**
   - Set up Azure ExpressRoute for a dedicated, private connection between the company's on-premises data center and Azure, ensuring low latency and high reliability.

6. **Content Delivery Network (CDN):**
   - Integrate Azure CDN to cache static content (e.g., images, videos) at edge locations worldwide, reducing load on the web servers and improving user experience.

#### 2. **Global SaaS Application: Multi-Region Deployment**
**Scenario:**
A Software-as-a-Service (SaaS) provider offers a collaboration tool used by customers worldwide. The provider needs to ensure global availability and low latency for all users.

**Solution:**
1. **Multiple VNets:**
   - Create VNets in multiple Azure regions (e.g., East US, West Europe, Southeast Asia) to host application instances close to users.

2. **Traffic Manager:**
   - Deploy Azure Traffic Manager to direct user traffic to the nearest or best-performing region based on routing methods like geographic or performance routing.

3. **Global VNet Peering:**
   - Use Global VNet Peering to connect VNets across different regions, enabling seamless communication between regional instances.

4. **Database Replication:**
   - Set up Azure SQL Database with Active Geo-Replication to replicate databases across regions, ensuring data availability and disaster recovery.

5. **Azure Front Door:**
   - Implement Azure Front Door as a global load balancer and application accelerator to distribute traffic efficiently, handle failovers, and provide SSL termination.

6. **DDoS Protection:**
   - Enable Azure DDoS Protection to safeguard against distributed denial of service attacks, ensuring the application's availability during attack attempts.

#### 3. **Hybrid Cloud Environment: Integration with On-Premises Infrastructure**
**Scenario:**
A financial services company wants to extend its on-premises data center to Azure for disaster recovery and additional compute capacity. They need a secure and reliable hybrid cloud setup.

**Solution:**
1. **Site-to-Site VPN:**
   - Configure a Site-to-Site VPN to establish a secure and encrypted connection between the on-premises network and Azure VNet.

2. **ExpressRoute:**
   - For enhanced performance and reliability, set up Azure ExpressRoute for a private connection between the on-premises data center and Azure.

3. **Azure Backup and Site Recovery:**
   - Implement Azure Backup to protect on-premises and Azure workloads.
   - Use Azure Site Recovery to replicate on-premises VMs to Azure for disaster recovery, ensuring business continuity.

4. **Identity Integration:**
   - Integrate on-premises Active Directory with Azure Active Directory using Azure AD Connect, providing a unified identity solution for seamless access management.

5. **Azure Bastion:**
   - Deploy Azure Bastion for secure RDP/SSH access to Azure VMs directly from the Azure portal without exposing VMs to the public internet.

6. **Network Monitoring:**
   - Use Azure Network Watcher to monitor and diagnose network issues, ensuring the hybrid environment operates smoothly.

### Conclusion
These real-world examples demonstrate how Azure networking services can be leveraged to build robust, scalable, and secure network solutions tailored to specific business needs. Whether it's ensuring high availability for an e-commerce platform, enabling global reach for a SaaS application, or integrating on-premises infrastructure with the cloud, Azure provides a comprehensive suite of networking tools to address diverse scenarios.


Below are Terraform scripts for each of the real-world scenarios mentioned. These scripts illustrate how to provision Azure resources using Terraform. Ensure you have the necessary permissions and prerequisites (e.g., Terraform installed, Azure CLI configured, and an Azure account) before running these scripts.

### 1. E-Commerce Platform: High Availability and Scalability

```hcl
# Variables
variable "resource_group_name" {
  default = "ecommerce-rg"
}

variable "location" {
  default = "East US"
}

variable "vnet_name" {
  default = "ecommerce-vnet"
}

variable "subnet_web" {
  default = "web-subnet"
}

variable "subnet_app" {
  default = "app-subnet"
}

variable "subnet_db" {
  default = "db-subnet"
}

variable "address_space" {
  default = ["10.0.0.0/16"]
}

variable "subnet_web_prefix" {
  default = "10.0.1.0/24"
}

variable "subnet_app_prefix" {
  default = "10.0.2.0/24"
}

variable "subnet_db_prefix" {
  default = "10.0.3.0/24"
}

# Resource Group
resource "azurerm_resource_group" "ecommerce" {
  name     = var.resource_group_name
  location = var.location
}

# Virtual Network
resource "azurerm_virtual_network" "ecommerce_vnet" {
  name                = var.vnet_name
  address_space       = var.address_space
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
}

# Subnets
resource "azurerm_subnet" "web" {
  name                 = var.subnet_web
  resource_group_name  = azurerm_resource_group.ecommerce.name
  virtual_network_name = azurerm_virtual_network.ecommerce_vnet.name
  address_prefixes     = [var.subnet_web_prefix]
}

resource "azurerm_subnet" "app" {
  name                 = var.subnet_app
  resource_group_name  = azurerm_resource_group.ecommerce.name
  virtual_network_name = azurerm_virtual_network.ecommerce_vnet.name
  address_prefixes     = [var.subnet_app_prefix]
}

resource "azurerm_subnet" "db" {
  name                 = var.subnet_db
  resource_group_name  = azurerm_resource_group.ecommerce.name
  virtual_network_name = azurerm_virtual_network.ecommerce_vnet.name
  address_prefixes     = [var.subnet_db_prefix]
}

# Network Security Group for Web Subnet
resource "azurerm_network_security_group" "web_nsg" {
  name                = "web-nsg"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
}

resource "azurerm_network_security_rule" "web_allow_inbound" {
  name                        = "allow-http-https-inbound"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_ranges     = ["80", "443"]
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.web_nsg.name
}

resource "azurerm_subnet_network_security_group_association" "web_nsg_assoc" {
  subnet_id                 = azurerm_subnet.web.id
  network_security_group_id = azurerm_network_security_group.web_nsg.id
}

# Public IP for Load Balancer
resource "azurerm_public_ip" "lb_public_ip" {
  name                = "lb-public-ip"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Load Balancer
resource "azurerm_lb" "load_balancer" {
  name                = "ecommerce-lb"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  sku                 = "Standard"
  frontend_ip_configuration {
    name                 = "frontend-config"
    public_ip_address_id = azurerm_public_ip.lb_public_ip.id
  }
}

# Backend Pool
resource "azurerm_lb_backend_address_pool" "backend_pool" {
  name                = "backend-pool"
  resource_group_name = azurerm_resource_group.ecommerce.name
  loadbalancer_id     = azurerm_lb.load_balancer.id
}

# Health Probe
resource "azurerm_lb_probe" "http_probe" {
  name                = "http-probe"
  resource_group_name = azurerm_resource_group.ecommerce.name
  loadbalancer_id     = azurerm_lb.load_balancer.id
  protocol            = "Http"
  request_path        = "/"
  port                = 80
  interval_in_seconds = 15
  number_of_probes    = 2
}

# Load Balancing Rule
resource "azurerm_lb_rule" "lb_rule" {
  name                            = "http-rule"
  resource_group_name             = azurerm_resource_group.ecommerce.name
  loadbalancer_id                 = azurerm_lb.load_balancer.id
  frontend_ip_configuration_name  = "frontend-config"
  backend_address_pool_id         = azurerm_lb_backend_address_pool.backend_pool.id
  probe_id                        = azurerm_lb_probe.http_probe.id
  protocol                        = "Tcp"
  frontend_port                   = 80
  backend_port                    = 80
  idle_timeout_in_minutes         = 4
  enable_floating_ip              = false
  load_distribution               = "Default"
}

# Virtual Machine Scale Set
resource "azurerm_virtual_machine_scale_set" "vmss" {
  name                = "ecommerce-vmss"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  upgrade_policy_mode = "Manual"

  sku {
    name     = "Standard_DS1_v2"
    tier     = "Standard"
    capacity = 2
  }

  network_profile {
    name    = "networkprofile"
    primary = true

    ip_configuration {
      name      = "ipconfig"
      subnet_id = azurerm_subnet.web.id
      primary   = true

      load_balancer_backend_address_pool_ids = [
        azurerm_lb_backend_address_pool.backend_pool.id
      ]
    }
  }

  os_profile {
    computer_name_prefix = "ecommercevm"
    admin_username       = "adminuser"
    admin_password       = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  storage_profile_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_profile_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  storage_profile_data_disk {
    lun           = 0
    caching       = "ReadWrite"
    create_option = "Empty"
    disk_size_gb  = 10
  }
}
```

### 2. Global SaaS Application: Multi-Region Deployment

```hcl
# Variables
variable "resource_group_name" {
  default = "saas-rg"
}

variable "location1" {
  default = "East US"
}

variable "location2" {
  default = "West Europe"
}

variable "vnet_name1" {
  default = "saas-vnet-eastus"
}

variable "vnet_name2" {
  default = "saas-vnet-westeurope"
}

variable "subnet_name" {
  default = "saas-subnet"
}

variable "address_space1" {
  default = ["10.1.0.0/16"]
}

variable "address_space2" {
  default = ["10.2.0.0/16"]
}

variable "subnet_prefix" {
  default = "10.1.1.0/24"
}

# Resource Groups
resource "azurerm_resource_group" "saas_eastus" {
  name     = var.resource_group_name
  location = var.location1
}

resource "azurerm_resource_group" "saas_westeurope" {
  name     = "${var.resource_group_name}-we"
  location = var.location2
}

# Virtual Networks
resource "azurerm_virtual_network" "saas_vnet_eastus" {
  name                = var.vnet_name1
  address_space       = var.address_space1
  location            = azurerm_resource_group.saas_eastus.location
  resource_group_name = azurerm_resource_group.saas_eastus.name
}

resource "azurerm_virtual_network" "saas_vnet_westeurope" {
  name                = var.vnet_name2
  address_space       = var.address_space2
  location            = azurerm_resource_group.saas_westeurope.location
  resource_group_name = azurerm_resource_group.saas_westeurope.name
}

# Subnets
resource "azurerm_subnet" "saas_subnet_eastus" {
  name                 = var.subnet_name
  resource_group_name  =

 azurerm_resource_group.saas_eastus.name
  virtual_network_name = azurerm_virtual_network.saas_vnet_eastus.name
  address_prefixes     = [var.subnet_prefix]
}

resource "azurerm_subnet" "saas_subnet_westeurope" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.saas_westeurope.name
  virtual_network_name = azurerm_virtual_network.saas_vnet_westeurope.name
  address_prefixes     = [var.subnet_prefix]
}

# Virtual Machines in East US
resource "azurerm_virtual_machine" "saas_vm_eastus" {
  count               = 2
  name                = "saas-vm-eastus-${count.index}"
  location            = azurerm_resource_group.saas_eastus.location
  resource_group_name = azurerm_resource_group.saas_eastus.name
  network_interface_ids = [
    azurerm_network_interface.saas_nic_eastus[count.index].id
  ]
  vm_size             = "Standard_DS1_v2"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "saas-vm-eastus"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

resource "azurerm_network_interface" "saas_nic_eastus" {
  count               = 2
  name                = "saas-nic-eastus-${count.index}"
  location            = azurerm_resource_group.saas_eastus.location
  resource_group_name = azurerm_resource_group.saas_eastus.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.saas_subnet_eastus.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Virtual Machines in West Europe
resource "azurerm_virtual_machine" "saas_vm_westeurope" {
  count               = 2
  name                = "saas-vm-westeurope-${count.index}"
  location            = azurerm_resource_group.saas_westeurope.location
  resource_group_name = azurerm_resource_group.saas_westeurope.name
  network_interface_ids = [
    azurerm_network_interface.saas_nic_westeurope[count.index].id
  ]
  vm_size             = "Standard_DS1_v2"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "saas-vm-westeurope"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

resource "azurerm_network_interface" "saas_nic_westeurope" {
  count               = 2
  name                = "saas-nic-westeurope-${count.index}"
  location            = azurerm_resource_group.saas_westeurope.location
  resource_group_name = azurerm_resource_group.saas_westeurope.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.saas_subnet_westeurope.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Traffic Manager Profile
resource "azurerm_traffic_manager_profile" "saas_tm" {
  name                = "saas-traffic-manager"
  resource_group_name = azurerm_resource_group.saas_eastus.name
  location            = "global"
  profile_status      = "Enabled"
  traffic_routing_method = "Performance"

  dns_config {
    relative_name = "saas-tm"
    ttl           = 30
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }
}

resource "azurerm_traffic_manager_endpoint" "eastus_endpoint" {
  name                = "eastus-endpoint"
  resource_group_name = azurerm_resource_group.saas_eastus.name
  profile_name        = azurerm_traffic_manager_profile.saas_tm.name
  type                = "azureEndpoints"
  target_resource_id  = azurerm_virtual_machine.saas_vm_eastus[0].id
  endpoint_location   = azurerm_resource_group.saas_eastus.location
  priority            = 1
}

resource "azurerm_traffic_manager_endpoint" "westeurope_endpoint" {
  name                = "westeurope-endpoint"
  resource_group_name = azurerm_resource_group.saas_eastus.name
  profile_name        = azurerm_traffic_manager_profile.saas_tm.name
  type                = "azureEndpoints"
  target_resource_id  = azurerm_virtual_machine.saas_vm_westeurope[0].id
  endpoint_location   = azurerm_resource_group.saas_westeurope.location
  priority            = 2
}
```

### 3. Hybrid Cloud Environment: Integration with On-Premises Infrastructure

```hcl
# Variables
variable "resource_group_name" {
  default = "hybridcloud-rg"
}

variable "location" {
  default = "East US"
}

variable "vnet_name" {
  default = "hybrid-vnet"
}

variable "subnet_name" {
  default = "hybrid-subnet"
}

variable "address_space" {
  default = ["10.3.0.0/16"]
}

variable "subnet_prefix" {
  default = "10.3.1.0/24"
}

variable "vpn_gateway_sku" {
  default = "VpnGw1"
}

variable "local_network_gateway_name" {
  default = "onpremise-lng"
}

variable "onprem_address_space" {
  default = ["192.168.0.0/16"]
}

variable "onprem_ip_address" {
  default = "203.0.113.5"
}

variable "shared_key" {
  default = "abc123"
}

# Resource Group
resource "azurerm_resource_group" "hybridcloud" {
  name     = var.resource_group_name
  location = var.location
}

# Virtual Network
resource "azurerm_virtual_network" "hybrid_vnet" {
  name                = var.vnet_name
  address_space       = var.address_space
  location            = azurerm_resource_group.hybridcloud.location
  resource_group_name = azurerm_resource_group.hybridcloud.name
}

# Subnet
resource "azurerm_subnet" "hybrid_subnet" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.hybridcloud.name
  virtual_network_name = azurerm_virtual_network.hybrid_vnet.name
  address_prefixes     = [var.subnet_prefix]
}

# Public IP for VPN Gateway
resource "azurerm_public_ip" "vpn_public_ip" {
  name                = "vpn-public-ip"
  location            = azurerm_resource_group.hybridcloud.location
  resource_group_name = azurerm_resource_group.hybridcloud.name
  allocation_method   = "Dynamic"
}

# VPN Gateway
resource "azurerm_virtual_network_gateway" "vpn_gateway" {
  name                = "vpn-gateway"
  location            = azurerm_resource_group.hybridcloud.location
  resource_group_name = azurerm_resource_group.hybridcloud.name

  type     = "Vpn"
  vpn_type = "RouteBased"
  sku      = var.vpn_gateway_sku

  ip_configuration {
    name                          = "vpn-gateway-ipconfig"
    public_ip_address_id          = azurerm_public_ip.vpn_public_ip.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.hybrid_subnet.id
  }

  vpn_client_configuration {
    address_space = ["172.16.0.0/24"]
  }
}

# Local Network Gateway (On-Premises)
resource "azurerm_local_network_gateway" "onpremise_lng" {
  name                = var.local_network_gateway_name
  location            = azurerm_resource_group.hybridcloud.location
  resource_group_name = azurerm_resource_group.hybridcloud.name
  gateway_address     = var.onprem_ip_address
  address_space       = var.onprem_address_space
}

# Site-to-Site VPN Connection
resource "azurerm_virtual_network_gateway_connection" "site_to_site_vpn" {
  name                           = "site-to-site-vpn"
  location                       = azurerm_resource_group.hybridcloud.location
  resource_group_name            = azurerm_resource_group.hybridcloud.name
  virtual_network_gateway_id     = azurerm_virtual_network_gateway.vpn_gateway.id
  local_network_gateway_id       = azurerm_local_network_gateway.onpremise_lng.id
  type                           = "IPsec"
  connection_protocol            = "IKEv2"
  shared_key                    

 = var.shared_key
  enable_bgp                     = false
  use_policy_based_traffic_selectors = false
}

# Bastion Host for Secure VM Access
resource "azurerm_bastion_host" "bastion" {
  name                = "bastion-host"
  location            = azurerm_resource_group.hybridcloud.location
  resource_group_name = azurerm_resource_group.hybridcloud.name

  dns_name {
    name = "bastion"
  }

  ip_configuration {
    name                 = "bastion-ip-configuration"
    subnet_id            = azurerm_subnet.hybrid_subnet.id
    public_ip_address_id = azurerm_public_ip.vpn_public_ip.id
  }
}

# Virtual Machine in Hybrid Cloud
resource "azurerm_virtual_machine" "hybrid_vm" {
  name                  = "hybrid-vm"
  location              = azurerm_resource_group.hybridcloud.location
  resource_group_name   = azurerm_resource_group.hybridcloud.name
  network_interface_ids = [azurerm_network_interface.hybrid_nic.id]
  vm_size               = "Standard_DS1_v2"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hybrid-vm"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

resource "azurerm_network_interface" "hybrid_nic" {
  name                = "hybrid-nic"
  location            = azurerm_resource_group.hybridcloud.location
  resource_group_name = azurerm_resource_group.hybridcloud.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.hybrid_subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}
```

These Terraform scripts cover three different scenarios using Azure networking services. Each script provisions a set of resources tailored to the specific needs of an e-commerce platform, a global SaaS application, and a hybrid cloud environment. Adjust the variables and configurations according to your specific requirements and environment.
