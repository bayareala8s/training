High availability (HA) in Azure refers to the capability of a system or component to be continuously operational for a long duration of time. Azure provides several services and features that help in achieving high availability for applications and services. Here are the key concepts and strategies for implementing high availability in Azure:

### 1. **Availability Zones**

**Availability Zones** are physically separate locations within an Azure region. Each zone consists of one or more data centers equipped with independent power, cooling, and networking. Deploying applications across multiple Availability Zones can ensure high availability and protect applications and data from datacenter failures.

- **Zone Redundant Services:** Some Azure services, like Azure SQL Database and Azure Storage, can be configured to be zone-redundant, spreading replicas across multiple zones.
- **Regional Pairs:** Azure regions are paired to provide additional redundancy. This ensures that during planned maintenance, one region in the pair will be updated at a time, reducing the risk of downtime.

### 2. **Load Balancing**

**Load Balancers** distribute incoming network traffic across multiple backend resources, ensuring no single resource is overwhelmed, which enhances availability and reliability.

- **Azure Load Balancer:** Works at Layer 4 (transport layer) and can balance traffic for both public and internal services.
- **Azure Application Gateway:** Operates at Layer 7 (application layer) and provides advanced routing and web application firewall capabilities.
- **Traffic Manager:** DNS-based traffic load balancer that distributes traffic to different Azure regions, providing global high availability.

### 3. **Redundancy and Replication**

**Redundancy and Replication** are critical for high availability by ensuring that data and services are duplicated across different locations to prevent data loss or service interruption.

- **Geo-Redundant Storage (GRS):** Azure Storage can be configured to replicate data to a secondary region, providing a durable copy of data in case of a regional outage.
- **SQL Database Replication:** Azure SQL Database offers options like Active Geo-Replication and Auto-Failover Groups to replicate databases across multiple regions for high availability.

### 4. **Virtual Machine Availability Sets**

**Availability Sets** ensure that VMs deployed within them are distributed across multiple isolated hardware nodes in a cluster. This strategy protects applications against hardware failures.

- **Fault Domains:** These are logical groupings of hardware to avoid single points of failure within an availability set.
- **Update Domains:** These group VMs in a manner that allows updates and patches to be applied without downtime to the entire set.

### 5. **Azure Site Recovery**

**Azure Site Recovery** is a disaster recovery service that ensures applications remain available during planned and unplanned outages by replicating workloads to a secondary location.

- **Failover and Failback:** In the event of a primary site failure, Site Recovery can failover to the secondary site and later fail back to the primary site once it is operational.
- **Application Consistency:** Ensures that data is consistent and applications can recover without data loss.

### 6. **SQL Database High Availability**

Azure SQL Database provides built-in high availability with features like:

- **Zone-Redundant Configurations:** Databases can be configured to automatically replicate across availability zones.
- **Failover Groups:** Enable automatic failover of a group of databases to a secondary region.
- **Active Geo-Replication:** Allows for readable secondary databases in different regions for both high availability and load balancing read operations.

### 7. **Managed Disks**

Azure Managed Disks offer high availability with options like:

- **Locally Redundant Storage (LRS):** Synchronously replicates data within a single region.
- **Zone-Redundant Storage (ZRS):** Synchronously replicates data across three Availability Zones in a region.

### 8. **Kubernetes and Containers**

**Azure Kubernetes Service (AKS)** provides high availability for containerized applications with features like:

- **Cluster Nodes Spread:** Nodes can be spread across multiple availability zones for fault tolerance.
- **Pod Replication:** Ensures that multiple instances of a pod are running to handle traffic even if some instances fail.

### 9. **Service-Level Agreements (SLAs)**

Azure provides SLAs for many of its services, which guarantee a certain level of uptime and availability. Understanding these SLAs is crucial for designing high-availability solutions.

- **VMs:** 99.9% availability SLA when using Availability Sets or Availability Zones.
- **Azure SQL Database:** 99.99% availability for single databases and elastic pools.
- **Azure Storage:** 99.9% availability for standard storage accounts.

### Summary

Achieving high availability in Azure involves a combination of deploying services across multiple Availability Zones, using load balancers, ensuring data redundancy and replication, leveraging built-in high availability features of Azure services, and understanding and planning according to Azure's SLAs. These strategies help ensure that applications remain operational, minimize downtime, and provide a resilient infrastructure capable of handling failures and disruptions.


### Real-World Examples of High Availability in Azure

#### 1. **E-Commerce Platform**

**Scenario:** An e-commerce company needs to ensure that their online store is always available, especially during peak shopping times like Black Friday or holiday sales.

**Solution:**

- **Azure Regions and Availability Zones:** The platform is deployed across multiple Azure regions with each region using Availability Zones to ensure resilience against data center failures.
- **Azure Traffic Manager:** Used to direct user traffic to the nearest available region, improving performance and ensuring availability even if one region fails.
- **Azure SQL Database with Active Geo-Replication:** The product catalog and user data are replicated across multiple regions, allowing for read and write operations to continue seamlessly if the primary database fails.
- **Azure Application Gateway:** Provides load balancing and a web application firewall (WAF) to protect against malicious attacks and distribute traffic evenly across multiple web servers.
- **Azure Site Recovery:** Configured to replicate critical virtual machines and services to a secondary region for disaster recovery.

**Outcome:** The e-commerce platform maintains high availability and can handle increased traffic without downtime, ensuring a smooth shopping experience for users.

#### 2. **Financial Services Application**

**Scenario:** A financial services company needs to ensure their banking application is always available to customers for transactions and account management.

**Solution:**

- **Availability Sets and Zones:** Virtual machines hosting the banking application are placed in Availability Sets and spread across multiple Availability Zones to protect against hardware and zone failures.
- **Azure Load Balancer:** Distributes traffic across multiple VMs to ensure no single VM is overwhelmed and provides automatic failover in case a VM goes down.
- **Azure Cosmos DB:** Used for storing transactional data with multi-region writes enabled, ensuring data is always available and consistent across different regions.
- **Azure Functions and Logic Apps:** Implement serverless architecture for processing transactions, with functions distributed across multiple regions to ensure they are always available.
- **Azure Backup:** Regular backups of critical data to ensure that in the event of data loss, recovery can be performed quickly and efficiently.

**Outcome:** The financial services application achieves near 100% availability, ensuring that customers can always access their accounts and perform transactions without interruption.

#### 3. **Healthcare Management System**

**Scenario:** A healthcare provider needs a reliable system for managing patient records, scheduling, and telemedicine services.

**Solution:**

- **Azure Kubernetes Service (AKS):** The application is containerized and deployed on AKS, with clusters spread across multiple availability zones for high availability.
- **Azure SQL Database with Auto-Failover Groups:** Patient records and appointment data are stored in SQL databases configured with auto-failover groups, ensuring seamless failover to a secondary region if the primary region fails.
- **Azure Front Door:** Provides global load balancing and secure, fast access to the application, directing users to the nearest available backend.
- **Azure Monitor and Application Insights:** Continuously monitor application performance and availability, enabling quick identification and resolution of issues.
- **Azure Active Directory (AD):** Ensures secure and reliable user authentication and authorization, with multiple replicas to ensure high availability.

**Outcome:** The healthcare management system remains highly available, ensuring that patients and healthcare providers can always access critical services and data without interruptions.

#### 4. **Media Streaming Service**

**Scenario:** A media company needs to ensure their streaming service is always available to users worldwide, especially during live events.

**Solution:**

- **Azure Media Services:** Used to encode, store, and stream media content, with redundancy built-in to handle high traffic volumes and ensure content is always available.
- **Content Delivery Network (CDN):** Distributes media content across multiple edge locations globally, ensuring low latency and high availability for users.
- **Azure Cosmos DB:** Stores user preferences, watch history, and metadata, with multi-region replication to ensure fast access and high availability.
- **Azure Virtual Machines with Availability Zones:** Backend services and databases are hosted on VMs spread across multiple zones to protect against zone failures.
- **Azure SignalR Service:** Ensures real-time communication and updates during live events, with multiple instances to handle high traffic.

**Outcome:** The media streaming service delivers consistent, high-quality streaming experiences to users worldwide, even during peak usage times and live events.

These examples illustrate how Azure's high availability features and services can be leveraged to build robust, resilient applications that can withstand failures and provide uninterrupted service to users.


Here are Terraform scripts for each of the real-world examples:

### 1. **E-Commerce Platform**

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ecommerce" {
  name     = "ecommerce-resources"
  location = "West Europe"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "ecommerce-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "ecommerce-subnet"
  resource_group_name  = azurerm_resource_group.ecommerce.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "ecommerce_ip" {
  name                = "ecommerce-public-ip"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_lb" "ecommerce_lb" {
  name                = "ecommerce-lb"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "publicIPAddress"
    public_ip_address_id = azurerm_public_ip.ecommerce_ip.id
  }
}

resource "azurerm_lb_backend_address_pool" "ecommerce_pool" {
  loadbalancer_id = azurerm_lb.ecommerce_lb.id
  name            = "ecommerce-backend-pool"
}

resource "azurerm_availability_set" "ecommerce_avset" {
  name                = "ecommerce-avset"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  platform_fault_domain_count  = 2
  platform_update_domain_count = 2
  managed                = true
}

resource "azurerm_network_interface" "ecommerce_nic" {
  count               = 2
  name                = "ecommerce-nic-${count.index}"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    load_balancer_backend_address_pools_ids = [azurerm_lb_backend_address_pool.ecommerce_pool.id]
  }
}

resource "azurerm_windows_virtual_machine" "ecommerce_vm" {
  count               = 2
  name                = "ecommerce-vm-${count.index}"
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  size                = "Standard_DS1_v2"
  admin_username      = "adminuser"
  admin_password      = "Password1234!"
  availability_set_id = azurerm_availability_set.ecommerce_avset.id

  network_interface_ids = [azurerm_network_interface.ecommerce_nic[count.index].id]

  os_disk {
    name              = "osdisk-${count.index}"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }
}
```

### 2. **Financial Services Application**

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "finance" {
  name     = "finance-resources"
  location = "East US"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "finance-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "finance-subnet"
  resource_group_name  = azurerm_resource_group.finance.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_public_ip" "finance_ip" {
  name                = "finance-public-ip"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_lb" "finance_lb" {
  name                = "finance-lb"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "publicIPAddress"
    public_ip_address_id = azurerm_public_ip.finance_ip.id
  }
}

resource "azurerm_lb_backend_address_pool" "finance_pool" {
  loadbalancer_id = azurerm_lb.finance_lb.id
  name            = "finance-backend-pool"
}

resource "azurerm_availability_set" "finance_avset" {
  name                = "finance-avset"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
  platform_fault_domain_count  = 2
  platform_update_domain_count = 2
  managed                = true
}

resource "azurerm_network_interface" "finance_nic" {
  count               = 2
  name                = "finance-nic-${count.index}"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    load_balancer_backend_address_pools_ids = [azurerm_lb_backend_address_pool.finance_pool.id]
  }
}

resource "azurerm_linux_virtual_machine" "finance_vm" {
  count               = 2
  name                = "finance-vm-${count.index}"
  resource_group_name = azurerm_resource_group.finance.name
  location            = azurerm_resource_group.finance.location
  size                = "Standard_B1ms"
  admin_username      = "adminuser"
  admin_password      = "Password1234!"
  availability_set_id = azurerm_availability_set.finance_avset.id

  network_interface_ids = [azurerm_network_interface.finance_nic[count.index].id]

  os_disk {
    name              = "osdisk-${count.index}"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
```

### 3. **Healthcare Management System**

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "healthcare" {
  name     = "healthcare-resources"
  location = "Central US"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "healthcare-aks"
  location            = azurerm_resource_group.healthcare.location
  resource_group_name = azurerm_resource_group.healthcare.name
  dns_prefix          = "healthcareaks"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    load_balancer_sku = "Standard"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "secondary" {
  name                = "secondary"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size             = "Standard_DS2_v2"
  node_count          = 3
}

resource "azurerm_public_ip" "aks_ip" {
  name                = "aks-public-ip"
  location            = azurerm_resource_group.healthcare.location
  resource_group_name = azurerm_resource_group.healthcare.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_application_gateway" "appgw" {
  name                = "healthcare-appgw"
  location            = azurerm_resource_group.healthcare.location
  resource_group_name = azurerm_resource_group.healthcare.name
  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "appgw-ipcfg"
    subnet_id = azurerm_subnet.subnet.id
  }

  frontend_ip_configuration {
    name                 = "appgw-feipcfg"
    public_ip_address_id = azurerm_public_ip.aks_ip.id
  }

 

 frontend_port {
    name = "appgw-feport"
    port = 80
  }

  backend_address_pool {
    name = "appgw-beap"
  }

  backend_http_settings {
    name                  = "appgw-behttpsettings"
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 20
  }

  http_listener {
    name                           = "appgw-httplistener"
    frontend_ip_configuration_name = "appgw-feipcfg"
    frontend_port_name             = "appgw-feport"
    protocol                       = "Http"
  }

  request_routing_rule {
    name                       = "appgw-routetourl"
    rule_type                  = "Basic"
    http_listener_name         = "appgw-httplistener"
    backend_address_pool_name  = "appgw-beap"
    backend_http_settings_name = "appgw-behttpsettings"
  }
}

resource "azurerm_sql_server" "sqlserver" {
  name                         = "healthcaresqlserver"
  resource_group_name          = azurerm_resource_group.healthcare.name
  location                     = azurerm_resource_group.healthcare.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "Password1234!"
}

resource "azurerm_sql_database" "sqldb" {
  name                = "healthcaresqldb"
  resource_group_name = azurerm_sql_server.sqlserver.resource_group_name
  location            = azurerm_sql_server.sqlserver.location
  server_name         = azurerm_sql_server.sqlserver.name
  requested_service_objective_name = "S0"
}
```

### 4. **Media Streaming Service**

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "media" {
  name     = "media-resources"
  location = "South Central US"
}

resource "azurerm_storage_account" "media_storage" {
  name                     = "mediastorageacct"
  resource_group_name      = azurerm_resource_group.media.name
  location                 = azurerm_resource_group.media.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_media_services_account" "media_services" {
  name                = "mediaservicesacct"
  location            = azurerm_resource_group.media.location
  resource_group_name = azurerm_resource_group.media.name
  storage_account {
    id = azurerm_storage_account.media_storage.id
  }
}

resource "azurerm_media_transform" "media_transform" {
  name                = "mediatransform"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
  description         = "Media Transform"
  output {
    preset {
      preset_name = "AdaptiveStreaming"
    }
  }
}

resource "azurerm_media_streaming_policy" "media_policy" {
  name                = "mediapolicy"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
  no_encryption_enabled_protocols {
    download = true
    dash     = true
    hls      = true
    smooth_streaming = true
  }
}

resource "azurerm_media_asset" "media_asset" {
  name                = "mediaasset"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
}

resource "azurerm_media_streaming_endpoint" "media_endpoint" {
  name                = "mediaendpoint"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
  scale_units         = 1
  host_name           = "media.streaming.endpoint"
}

resource "azurerm_traffic_manager_profile" "traffic_manager" {
  name                = "media-traffic-manager"
  resource_group_name = azurerm_resource_group.media.name
  location            = azurerm_resource_group.media.location
  profile_status      = "Enabled"
  traffic_routing_method = "Priority"
  dns_config {
    relative_name = "media"
    ttl           = 30
  }
  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }
}

resource "azurerm_traffic_manager_endpoint" "media_endpoint" {
  count                 = 2
  name                  = "media-endpoint-${count.index}"
  resource_group_name   = azurerm_traffic_manager_profile.traffic_manager.resource_group_name
  profile_name          = azurerm_traffic_manager_profile.traffic_manager.name
  type                  = "azureEndpoints"
  target_resource_id    = azurerm_media_streaming_endpoint.media_endpoint.id
  endpoint_location     = element(["East US", "West US"], count.index)
  priority              = count.index + 1
}
```

These scripts provide a starting point for deploying high availability solutions on Azure for different use cases. You may need to adjust the scripts to fit specific requirements or constraints.


Sure, here is a detailed explanation of each of the Terraform scripts for the provided real-world examples.

### 1. **E-Commerce Platform**

#### Terraform Script Explanation:

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider Configuration:** Specifies that we are using Azure as our cloud provider.

```hcl
resource "azurerm_resource_group" "ecommerce" {
  name     = "ecommerce-resources"
  location = "West Europe"
}
```
- **Resource Group:** Creates a resource group named "ecommerce-resources" in the "West Europe" region to group all related resources.

```hcl
resource "azurerm_virtual_network" "vnet" {
  name                = "ecommerce-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
}
```
- **Virtual Network:** Defines a virtual network named "ecommerce-vnet" with the address space "10.0.0.0/16" in the specified resource group and location.

```hcl
resource "azurerm_subnet" "subnet" {
  name                 = "ecommerce-subnet"
  resource_group_name  = azurerm_resource_group.ecommerce.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}
```
- **Subnet:** Creates a subnet named "ecommerce-subnet" within the virtual network with the address prefix "10.0.1.0/24".

```hcl
resource "azurerm_public_ip" "ecommerce_ip" {
  name                = "ecommerce-public-ip"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  allocation_method   = "Static"
  sku                 = "Standard"
}
```
- **Public IP Address:** Allocates a static public IP address for the load balancer with the name "ecommerce-public-ip".

```hcl
resource "azurerm_lb" "ecommerce_lb" {
  name                = "ecommerce-lb"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "publicIPAddress"
    public_ip_address_id = azurerm_public_ip.ecommerce_ip.id
  }
}
```
- **Load Balancer:** Configures a load balancer named "ecommerce-lb" with the public IP address previously created.

```hcl
resource "azurerm_lb_backend_address_pool" "ecommerce_pool" {
  loadbalancer_id = azurerm_lb.ecommerce_lb.id
  name            = "ecommerce-backend-pool"
}
```
- **Backend Address Pool:** Creates a backend address pool for the load balancer to distribute traffic among multiple VMs.

```hcl
resource "azurerm_availability_set" "ecommerce_avset" {
  name                = "ecommerce-avset"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  platform_fault_domain_count  = 2
  platform_update_domain_count = 2
  managed                = true
}
```
- **Availability Set:** Ensures that the VMs are distributed across multiple fault and update domains to increase availability.

```hcl
resource "azurerm_network_interface" "ecommerce_nic" {
  count               = 2
  name                = "ecommerce-nic-${count.index}"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    load_balancer_backend_address_pools_ids = [azurerm_lb_backend_address_pool.ecommerce_pool.id]
  }
}
```
- **Network Interface:** Creates network interfaces for the VMs and associates them with the load balancer backend pool.

```hcl
resource "azurerm_windows_virtual_machine" "ecommerce_vm" {
  count               = 2
  name                = "ecommerce-vm-${count.index}"
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  size                = "Standard_DS1_v2"
  admin_username      = "adminuser"
  admin_password      = "Password1234!"
  availability_set_id = azurerm_availability_set.ecommerce_avset.id

  network_interface_ids = [azurerm_network_interface.ecommerce_nic[count.index].id]

  os_disk {
    name              = "osdisk-${count.index}"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }
}
```
- **Virtual Machines:** Creates two Windows virtual machines, ensuring they are part of the availability set and associated with the respective network interfaces.

### 2. **Financial Services Application**

#### Terraform Script Explanation:

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider Configuration:** Specifies that we are using Azure as our cloud provider.

```hcl
resource "azurerm_resource_group" "finance" {
  name     = "finance-resources"
  location = "East US"
}
```
- **Resource Group:** Creates a resource group named "finance-resources" in the "East US" region.

```hcl
resource "azurerm_virtual_network" "vnet" {
  name                = "finance-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
}
```
- **Virtual Network:** Defines a virtual network named "finance-vnet" with the address space "10.1.0.0/16".

```hcl
resource "azurerm_subnet" "subnet" {
  name                 = "finance-subnet"
  resource_group_name  = azurerm_resource_group.finance.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.1.1.0/24"]
}
```
- **Subnet:** Creates a subnet named "finance-subnet" within the virtual network with the address prefix "10.1.1.0/24".

```hcl
resource "azurerm_public_ip" "finance_ip" {
  name                = "finance-public-ip"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
  allocation_method   = "Static"
  sku                 = "Standard"
}
```
- **Public IP Address:** Allocates a static public IP address for the load balancer with the name "finance-public-ip".

```hcl
resource "azurerm_lb" "finance_lb" {
  name                = "finance-lb"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "publicIPAddress"
    public_ip_address_id = azurerm_public_ip.finance_ip.id
  }
}
```
- **Load Balancer:** Configures a load balancer named "finance-lb" with the public IP address previously created.

```hcl
resource "azurerm_lb_backend_address_pool" "finance_pool" {
  loadbalancer_id = azurerm_lb.finance_lb.id
  name            = "finance-backend-pool"
}
```
- **Backend Address Pool:** Creates a backend address pool for the load balancer to distribute traffic among multiple VMs.

```hcl
resource "azurerm_availability_set" "finance_avset" {
  name                = "finance-avset"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name
  platform_fault_domain_count  = 2
  platform_update_domain_count = 2
  managed                = true
}
```
- **Availability Set:** Ensures that the VMs are distributed across multiple fault and update domains to increase availability.

```hcl
resource "azurerm_network_interface" "finance_nic" {
  count               = 2
  name                = "finance-nic-${count.index}"
  location            = azurerm_resource_group.finance.location
  resource_group_name = azurerm_resource_group.finance.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    load_balancer_backend_address_pools_ids = [azurerm_lb_backend_address_pool.finance_pool.id]
  }
}
```
- **Network Interface:** Creates network interfaces for the VMs and associates them with the load balancer backend pool.

```hcl
resource "azurerm_linux_virtual_machine" "finance_vm" {
  count               = 2
  name                = "finance-vm-${count.index}"
  resource_group_name = azurerm_resource_group.finance.name
  location            =

 azurerm_resource_group.finance.location
  size                = "Standard_B1ms"
  admin_username      = "adminuser"
  admin_password      = "Password1234!"
  availability_set_id = azurerm_availability_set.finance_avset.id

  network_interface_ids = [azurerm_network_interface.finance_nic[count.index].id]

  os_disk {
    name              = "osdisk-${count.index}"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
```
- **Virtual Machines:** Creates two Linux virtual machines, ensuring they are part of the availability set and associated with the respective network interfaces.

### 3. **Healthcare Management System**

#### Terraform Script Explanation:

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider Configuration:** Specifies that we are using Azure as our cloud provider.

```hcl
resource "azurerm_resource_group" "healthcare" {
  name     = "healthcare-resources"
  location = "Central US"
}
```
- **Resource Group:** Creates a resource group named "healthcare-resources" in the "Central US" region.

```hcl
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "healthcare-aks"
  location            = azurerm_resource_group.healthcare.location
  resource_group_name = azurerm_resource_group.healthcare.name
  dns_prefix          = "healthcareaks"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    load_balancer_sku = "Standard"
  }
}
```
- **Kubernetes Cluster:** Creates an Azure Kubernetes Service (AKS) cluster with a default node pool of 3 nodes using "Standard_DS2_v2" VM size.

```hcl
resource "azurerm_kubernetes_cluster_node_pool" "secondary" {
  name                = "secondary"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size             = "Standard_DS2_v2"
  node_count          = 3
}
```
- **Secondary Node Pool:** Adds a secondary node pool to the AKS cluster to provide additional compute capacity.

```hcl
resource "azurerm_public_ip" "aks_ip" {
  name                = "aks-public-ip"
  location            = azurerm_resource_group.healthcare.location
  resource_group_name = azurerm_resource_group.healthcare.name
  allocation_method   = "Static"
  sku                 = "Standard"
}
```
- **Public IP Address:** Allocates a static public IP address for the Application Gateway.

```hcl
resource "azurerm_application_gateway" "appgw" {
  name                = "healthcare-appgw"
  location            = azurerm_resource_group.healthcare.location
  resource_group_name = azurerm_resource_group.healthcare.name
  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "appgw-ipcfg"
    subnet_id = azurerm_subnet.subnet.id
  }

  frontend_ip_configuration {
    name                 = "appgw-feipcfg"
    public_ip_address_id = azurerm_public_ip.aks_ip.id
  }

  frontend_port {
    name = "appgw-feport"
    port = 80
  }

  backend_address_pool {
    name = "appgw-beap"
  }

  backend_http_settings {
    name                  = "appgw-behttpsettings"
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 20
  }

  http_listener {
    name                           = "appgw-httplistener"
    frontend_ip_configuration_name = "appgw-feipcfg"
    frontend_port_name             = "appgw-feport"
    protocol                       = "Http"
  }

  request_routing_rule {
    name                       = "appgw-routetourl"
    rule_type                  = "Basic"
    http_listener_name         = "appgw-httplistener"
    backend_address_pool_name  = "appgw-beap"
    backend_http_settings_name = "appgw-behttpsettings"
  }
}
```
- **Application Gateway:** Configures an Application Gateway for load balancing traffic to the AKS cluster, with associated IP configurations, backend pools, and routing rules.

```hcl
resource "azurerm_sql_server" "sqlserver" {
  name                         = "healthcaresqlserver"
  resource_group_name          = azurerm_resource_group.healthcare.name
  location                     = azurerm_resource_group.healthcare.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "Password1234!"
}
```
- **SQL Server:** Creates an Azure SQL Server instance.

```hcl
resource "azurerm_sql_database" "sqldb" {
  name                = "healthcaresqldb"
  resource_group_name = azurerm_sql_server.sqlserver.resource_group_name
  location            = azurerm_sql_server.sqlserver.location
  server_name         = azurerm_sql_server.sqlserver.name
  requested_service_objective_name = "S0"
}
```
- **SQL Database:** Creates a SQL database within the SQL Server instance.

### 4. **Media Streaming Service**

#### Terraform Script Explanation:

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider Configuration:** Specifies that we are using Azure as our cloud provider.

```hcl
resource "azurerm_resource_group" "media" {
  name     = "media-resources"
  location = "South Central US"
}
```
- **Resource Group:** Creates a resource group named "media-resources" in the "South Central US" region.

```hcl
resource "azurerm_storage_account" "media_storage" {
  name                     = "mediastorageacct"
  resource_group_name      = azurerm_resource_group.media.name
  location                 = azurerm_resource_group.media.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **Storage Account:** Creates a storage account for storing media files with locally redundant storage (LRS).

```hcl
resource "azurerm_media_services_account" "media_services" {
  name                = "mediaservicesacct"
  location            = azurerm_resource_group.media.location
  resource_group_name = azurerm_resource_group.media.name
  storage_account {
    id = azurerm_storage_account.media_storage.id
  }
}
```
- **Media Services Account:** Configures a Media Services account linked to the storage account for media processing.

```hcl
resource "azurerm_media_transform" "media_transform" {
  name                = "mediatransform"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
  description         = "Media Transform"
  output {
    preset {
      preset_name = "AdaptiveStreaming"
    }
  }
}
```
- **Media Transform:** Defines a media transform for adaptive streaming using Azure Media Services.

```hcl
resource "azurerm_media_streaming_policy" "media_policy" {
  name                = "mediapolicy"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
  no_encryption_enabled_protocols {
    download = true
    dash     = true
    hls      = true
    smooth_streaming = true
  }
}
```
- **Streaming Policy:** Creates a streaming policy that supports multiple streaming protocols without encryption.

```hcl
resource "azurerm_media_asset" "media_asset" {
  name                = "mediaasset"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
}
```
- **Media Asset:** Creates a media asset for storing and managing media content.

```hcl
resource "azurerm_media_streaming_endpoint" "media_endpoint" {
  name                = "mediaendpoint"
  resource_group_name = azurerm_media_services_account.media_services.resource_group_name
  account_name        = azurerm_media_services_account.media_services.name
  scale_units         = 1
  host_name           = "media.streaming.endpoint"
}
```
- **Streaming Endpoint:** Configures a streaming endpoint to deliver media content to users.

```hcl
resource "azurerm_traffic_manager_profile" "traffic_manager" {
  name                = "media-traffic-manager"
  resource_group_name = azurerm_resource_group.media.name
  location            = azurerm_resource_group.media.location
  profile_status      = "Enabled"
  traffic_routing_method = "Priority"
  dns_config {
    relative_name = "media"
    ttl           = 30
  }
  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }
}
```
- **Traffic Manager Profile:** Creates a Traffic Manager profile to direct user traffic to the nearest available streaming

 endpoint based on priority.

```hcl
resource "azurerm_traffic_manager_endpoint" "media_endpoint" {
  count                 = 2
  name                  = "media-endpoint-${count.index}"
  resource_group_name   = azurerm_traffic_manager_profile.traffic_manager.resource_group_name
  profile_name          = azurerm_traffic_manager_profile.traffic_manager.name
  type                  = "azureEndpoints"
  target_resource_id    = azurerm_media_streaming_endpoint.media_endpoint.id
  endpoint_location     = element(["East US", "West US"], count.index)
  priority              = count.index + 1
}
```
- **Traffic Manager Endpoints:** Configures two Traffic Manager endpoints, one for "East US" and one for "West US", each with a different priority to ensure high availability.

These scripts provide the necessary configurations for setting up high availability solutions in Azure for different scenarios. Adjustments may be required to fit specific use cases or organizational requirements.



