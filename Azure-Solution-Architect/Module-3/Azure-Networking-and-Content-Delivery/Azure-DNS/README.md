Azure DNS is a hosting service for DNS domains, providing name resolution using Microsoft Azure infrastructure. By hosting your domains in Azure, you can manage your DNS records using the same credentials, APIs, tools, and billing as your other Azure services. Here's a detailed explanation:

### Key Features of Azure DNS:

1. **Reliability and Performance**: Azure DNS uses a global network of name servers to provide fast responses to DNS queries. The service is highly available, with multiple levels of redundancy to ensure your DNS is always available.

2. **Security**: Azure DNS integrates with Azure’s identity and access management (IAM) capabilities to control access to DNS records. You can define who has permission to manage DNS records for each domain.

3. **Scalability**: Azure DNS is designed to handle high volumes of DNS queries. It scales automatically to handle increased load without manual intervention.

4. **Integration with Azure Services**: You can easily integrate Azure DNS with other Azure services. For instance, if you are using Azure Traffic Manager, you can use Azure DNS to direct traffic to the optimal endpoint.

5. **Zone Management**: Azure DNS allows you to create and manage DNS zones, which are collections of DNS records for a specific domain. You can manage both public DNS zones (for domains reachable from the internet) and private DNS zones (for internal Azure resources).

6. **DNSSEC**: Azure DNS supports DNS Security Extensions (DNSSEC) for domains registered with third-party registrars, ensuring authenticity and integrity of DNS data.

### Components of Azure DNS:

1. **DNS Zones**: A DNS zone is a container for DNS records for a particular domain. Each zone represents a unique domain name and contains the DNS records for that domain.

2. **DNS Records**: These are individual entries within a DNS zone that map domain names to IP addresses, mail servers, and other resources. Common types of DNS records include A, AAAA, CNAME, MX, and TXT records.

3. **Name Servers**: Azure DNS provides a set of name servers that host your DNS zone and respond to DNS queries for your domain.

4. **DNS Queries**: These are requests made by clients to resolve domain names to IP addresses. Azure DNS handles these queries by responding with the appropriate DNS records.

### How Azure DNS Works:

1. **Creating a DNS Zone**: To start using Azure DNS, you first create a DNS zone in the Azure portal, which serves as the authoritative source for your domain’s DNS records.

2. **Adding DNS Records**: Once the DNS zone is created, you can add DNS records to the zone. These records define how DNS queries for your domain are handled.

3. **Configuring Domain Registrar**: After setting up the DNS zone and records, you need to update the name servers for your domain at your domain registrar to point to the Azure DNS name servers.

4. **DNS Resolution**: When a client makes a DNS query for your domain, the request is routed to Azure DNS. Azure DNS then resolves the query by responding with the appropriate DNS record.

### Use Cases for Azure DNS:

1. **Hosting Websites**: Use Azure DNS to manage the DNS records for your websites, ensuring high availability and fast response times for users accessing your site.

2. **Internal DNS Resolution**: Manage DNS records for internal Azure resources using private DNS zones. This can simplify network management within your Azure environment.

3. **Traffic Management**: Combine Azure DNS with Azure Traffic Manager to route traffic based on performance, priority, or geographical location, ensuring optimal user experience.

4. **Hybrid Cloud Solutions**: Use Azure DNS to manage DNS records for a hybrid cloud environment, providing consistent name resolution for resources across on-premises and cloud environments.

### Managing Azure DNS:

1. **Azure Portal**: You can manage DNS zones and records using the Azure portal’s graphical interface.

2. **Azure CLI**: Use Azure Command-Line Interface (CLI) for scripting and automating DNS management tasks.

3. **Azure PowerShell**: Manage DNS records and zones using Azure PowerShell for advanced automation and scripting capabilities.

4. **REST API**: Azure DNS provides a REST API for programmatic access to DNS management features, allowing integration with custom applications and workflows.

### Pricing:

Azure DNS pricing is based on the number of DNS zones and the number of DNS queries processed. There are separate charges for public and private DNS zones. Detailed pricing information is available on the Azure website.

In summary, Azure DNS is a powerful and flexible DNS hosting service that integrates seamlessly with other Azure services, offering high reliability, security, and scalability for managing your domain’s DNS records.

Certainly! Here are some real-world examples of how organizations can use Azure DNS to solve various business challenges:

### Example 1: Hosting a Corporate Website

**Company**: Contoso Ltd.

**Scenario**: Contoso Ltd. wants to host its corporate website on Azure.

**Solution**:
1. **DNS Zone Creation**: Contoso creates a DNS zone for `contoso.com` in Azure DNS.
2. **DNS Records Setup**: Contoso adds various DNS records to manage its website and email services:
   - A record for `www.contoso.com` pointing to the IP address of the Azure web server.
   - MX records for `contoso.com` to handle email routing.
   - CNAME records for subdomains like `blog.contoso.com` and `shop.contoso.com`.
3. **Domain Registrar Configuration**: Contoso updates its domain registrar to use Azure DNS name servers.
4. **Benefits**: By using Azure DNS, Contoso ensures high availability and fast DNS resolution for its website visitors, leveraging Azure’s global infrastructure.

### Example 2: Internal Application Development

**Company**: Fabrikam Inc.

**Scenario**: Fabrikam Inc. is developing an internal application hosted on Azure and needs private DNS resolution for its virtual network.

**Solution**:
1. **Private DNS Zone**: Fabrikam creates a private DNS zone `fabrikam.internal` in Azure DNS.
2. **DNS Records for Internal Services**: Fabrikam adds DNS records for various internal services:
   - A records for internal APIs, databases, and microservices.
3. **Virtual Network Link**: Fabrikam links the private DNS zone to its Azure virtual network.
4. **Benefits**: Developers and applications within Fabrikam’s virtual network can resolve internal DNS names to IP addresses securely and efficiently, facilitating communication between services without exposing them to the public internet.

### Example 3: Global Traffic Management

**Company**: Adventure Works

**Scenario**: Adventure Works has a global customer base and needs to ensure fast and reliable access to its online store.

**Solution**:
1. **Traffic Manager Integration**: Adventure Works uses Azure Traffic Manager in conjunction with Azure DNS.
2. **DNS Zone for Online Store**: Adventure Works creates a DNS zone for `adventure-works.com`.
3. **Traffic Manager Profile**: Adventure Works configures a Traffic Manager profile to route traffic based on geographic location, performance, or priority.
4. **DNS Records Setup**: DNS records are added to point `www.adventure-works.com` to the Traffic Manager endpoint.
5. **Benefits**: Customers accessing `adventure-works.com` are directed to the nearest or most responsive Azure region, improving website performance and reliability.

### Example 4: Hybrid Cloud DNS Management

**Company**: Tailspin Toys

**Scenario**: Tailspin Toys operates a hybrid cloud environment and needs consistent DNS management across its on-premises and Azure resources.

**Solution**:
1. **Public and Private DNS Zones**: Tailspin Toys sets up both public and private DNS zones in Azure DNS.
2. **DNS Records for Hybrid Environment**:
   - Public DNS records for `tailspintoys.com` pointing to services hosted on Azure.
   - Private DNS records for `internal.tailspintoys.com` for on-premises resources.
3. **DNS Forwarding**: Tailspin Toys configures DNS forwarding rules to ensure seamless resolution between on-premises and cloud resources.
4. **Benefits**: Tailspin Toys achieves consistent DNS management, simplified network administration, and improved resource accessibility across its hybrid environment.

### Example 5: Disaster Recovery and Failover

**Company**: Northwind Traders

**Scenario**: Northwind Traders wants to implement a robust disaster recovery solution for its critical applications.

**Solution**:
1. **Primary and Secondary Zones**: Northwind Traders sets up primary and secondary DNS zones in different Azure regions.
2. **DNS Records Replication**: DNS records are replicated between the primary and secondary zones to ensure consistency.
3. **Failover Configuration**: Azure Traffic Manager is configured for failover, directing traffic to the secondary region if the primary region becomes unavailable.
4. **Benefits**: In the event of a disaster, DNS queries are automatically redirected to the secondary region, ensuring business continuity and minimizing downtime.

These examples demonstrate the versatility and power of Azure DNS in managing DNS needs for various scenarios, from simple website hosting to complex hybrid and global traffic management solutions.


Certainly! Below are Terraform scripts for setting up Azure DNS for the scenarios mentioned:

### Example 1: Hosting a Corporate Website

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "contoso-rg"
  location = "West US"
}

resource "azurerm_dns_zone" "contoso" {
  name                = "contoso.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_dns_a_record" "www" {
  name                = "www"
  zone_name           = azurerm_dns_zone.contoso.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["10.0.0.1"]
}

resource "azurerm_dns_mx_record" "mail" {
  name                = "@"
  zone_name           = azurerm_dns_zone.contoso.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  record {
    preference = 10
    exchange   = "mail.contoso.com"
  }
}

resource "azurerm_dns_cname_record" "blog" {
  name                = "blog"
  zone_name           = azurerm_dns_zone.contoso.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  record              = "blog.azurewebsites.net"
}
```

### Example 2: Internal Application Development

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "fabrikam-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "fabrikam-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone" "private_zone" {
  name                = "fabrikam.internal"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_a_record" "api" {
  name                = "api"
  zone_name           = azurerm_private_dns_zone.private_zone.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["10.0.0.4"]
}

resource "azurerm_private_dns_zone_virtual_network_link" "vnet_link" {
  name                  = "vnet-link"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.private_zone.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  registration_enabled  = true
}
```

### Example 3: Global Traffic Management

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "adventure-works-rg"
  location = "West Europe"
}

resource "azurerm_dns_zone" "zone" {
  name                = "adventure-works.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "tm-profile"
  resource_group_name = azurerm_resource_group.rg.name
  location            = "global"

  dns_config {
    relative_name = "www"
    ttl           = 300
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  traffic_routing_method = "Performance"
}

resource "azurerm_traffic_manager_endpoint" "primary" {
  name                = "primary-endpoint"
  resource_group_name = azurerm_resource_group.rg.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.zone.id
  endpoint_location   = "West Europe"
  priority            = 1
}

resource "azurerm_traffic_manager_endpoint" "secondary" {
  name                = "secondary-endpoint"
  resource_group_name = azurerm_resource_group.rg.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.zone.id
  endpoint_location   = "East US"
  priority            = 2
}
```

### Example 4: Hybrid Cloud DNS Management

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "tailspintoys-rg"
  location = "Central US"
}

resource "azurerm_dns_zone" "public_zone" {
  name                = "tailspintoys.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone" "private_zone" {
  name                = "internal.tailspintoys.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_a_record" "internal_api" {
  name                = "api"
  zone_name           = azurerm_private_dns_zone.private_zone.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["192.168.0.4"]
}

resource "azurerm_dns_a_record" "public_api" {
  name                = "api"
  zone_name           = azurerm_dns_zone.public_zone.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["13.92.173.1"]
}
```

### Example 5: Disaster Recovery and Failover

**Terraform Script:**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg_primary" {
  name     = "northwind-primary-rg"
  location = "West US"
}

resource "azurerm_resource_group" "rg_secondary" {
  name     = "northwind-secondary-rg"
  location = "East US"
}

resource "azurerm_dns_zone" "primary_zone" {
  name                = "northwindtraders.com"
  resource_group_name = azurerm_resource_group.rg_primary.name
}

resource "azurerm_dns_zone" "secondary_zone" {
  name                = "northwindtraders.com"
  resource_group_name = azurerm_resource_group.rg_secondary.name
}

resource "azurerm_dns_a_record" "www_primary" {
  name                = "www"
  zone_name           = azurerm_dns_zone.primary_zone.name
  resource_group_name = azurerm_resource_group.rg_primary.name
  ttl                 = 300
  records             = ["10.0.0.1"]
}

resource "azurerm_dns_a_record" "www_secondary" {
  name                = "www"
  zone_name           = azurerm_dns_zone.secondary_zone.name
  resource_group_name = azurerm_resource_group.rg_secondary.name
  ttl                 = 300
  records             = ["10.0.1.1"]
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "northwind-tm-profile"
  resource_group_name = azurerm_resource_group.rg_primary.name
  location            = "global"

  dns_config {
    relative_name = "www"
    ttl           = 300
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  traffic_routing_method = "Priority"
}

resource "azurerm_traffic_manager_endpoint" "primary" {
  name                = "primary-endpoint"
  resource_group_name = azurerm_resource_group.rg_primary.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.primary_zone.id
  endpoint_location   = "West US"
  priority            = 1
}

resource "azurerm_traffic_manager_endpoint" "secondary" {
  name                = "secondary-endpoint"
  resource_group_name = azurerm_resource_group.rg_secondary.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.secondary_zone.id
  endpoint_location   = "East US"
  priority            = 2
}
```

These scripts provide a starting point for each scenario. You may need to adjust them according to your specific requirements and infrastructure.


Sure! Below is a detailed explanation of the Terraform scripts provided for each scenario.

### Example 1: Hosting a Corporate Website

**Scenario**: Contoso Ltd. wants to host its corporate website on Azure.

**Terraform Script**:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "contoso-rg"
  location = "West US"
}

resource "azurerm_dns_zone" "contoso" {
  name                = "contoso.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_dns_a_record" "www" {
  name                = "www"
  zone_name           = azurerm_dns_zone.contoso.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["10.0.0.1"]
}

resource "azurerm_dns_mx_record" "mail" {
  name                = "@"
  zone_name           = azurerm_dns_zone.contoso.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  record {
    preference = 10
    exchange   = "mail.contoso.com"
  }
}

resource "azurerm_dns_cname_record" "blog" {
  name                = "blog"
  zone_name           = azurerm_dns_zone.contoso.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  record              = "blog.azurewebsites.net"
}
```

**Explanation**:
1. **Provider Configuration**: The script starts by specifying the Azure provider (`azurerm`). The `features {}` block is required but can be empty for now.
2. **Resource Group**: A resource group named `contoso-rg` is created in the `West US` region.
3. **DNS Zone**: A DNS zone named `contoso.com` is created within the resource group.
4. **A Record**: An A record named `www` is created, pointing to the IP address `10.0.0.1`, with a TTL of 300 seconds.
5. **MX Record**: An MX record for the root domain (`@`) is created, directing email to `mail.contoso.com` with a priority of 10.
6. **CNAME Record**: A CNAME record for `blog` is created, pointing to `blog.azurewebsites.net`.

### Example 2: Internal Application Development

**Scenario**: Fabrikam Inc. needs private DNS resolution for its internal application hosted on Azure.

**Terraform Script**:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "fabrikam-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "fabrikam-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone" "private_zone" {
  name                = "fabrikam.internal"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_a_record" "api" {
  name                = "api"
  zone_name           = azurerm_private_dns_zone.private_zone.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["10.0.0.4"]
}

resource "azurerm_private_dns_zone_virtual_network_link" "vnet_link" {
  name                  = "vnet-link"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.private_zone.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  registration_enabled  = true
}
```

**Explanation**:
1. **Provider Configuration**: Specifies the Azure provider.
2. **Resource Group**: Creates a resource group named `fabrikam-rg` in the `East US` region.
3. **Virtual Network**: Creates a virtual network named `fabrikam-vnet` with an address space of `10.0.0.0/16`.
4. **Private DNS Zone**: Creates a private DNS zone named `fabrikam.internal`.
5. **A Record**: Creates an A record named `api` in the private DNS zone, pointing to the IP address `10.0.0.4`.
6. **VNet Link**: Links the private DNS zone to the virtual network, enabling DNS name resolution within the VNet.

### Example 3: Global Traffic Management

**Scenario**: Adventure Works needs to ensure fast and reliable access to its online store globally.

**Terraform Script**:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "adventure-works-rg"
  location = "West Europe"
}

resource "azurerm_dns_zone" "zone" {
  name                = "adventure-works.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "tm-profile"
  resource_group_name = azurerm_resource_group.rg.name
  location            = "global"

  dns_config {
    relative_name = "www"
    ttl           = 300
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  traffic_routing_method = "Performance"
}

resource "azurerm_traffic_manager_endpoint" "primary" {
  name                = "primary-endpoint"
  resource_group_name = azurerm_resource_group.rg.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.zone.id
  endpoint_location   = "West Europe"
  priority            = 1
}

resource "azurerm_traffic_manager_endpoint" "secondary" {
  name                = "secondary-endpoint"
  resource_group_name = azurerm_resource_group.rg.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.zone.id
  endpoint_location   = "East US"
  priority            = 2
}
```

**Explanation**:
1. **Provider Configuration**: Specifies the Azure provider.
2. **Resource Group**: Creates a resource group named `adventure-works-rg` in the `West Europe` region.
3. **DNS Zone**: Creates a DNS zone named `adventure-works.com`.
4. **Traffic Manager Profile**: Creates a Traffic Manager profile named `tm-profile` with a performance-based routing method. This profile routes traffic to the nearest endpoint based on performance.
5. **Primary Endpoint**: Creates a primary Traffic Manager endpoint in the `West Europe` region.
6. **Secondary Endpoint**: Creates a secondary Traffic Manager endpoint in the `East US` region.

### Example 4: Hybrid Cloud DNS Management

**Scenario**: Tailspin Toys operates a hybrid cloud environment and needs consistent DNS management.

**Terraform Script**:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "tailspintoys-rg"
  location = "Central US"
}

resource "azurerm_dns_zone" "public_zone" {
  name                = "tailspintoys.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone" "private_zone" {
  name                = "internal.tailspintoys.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_a_record" "internal_api" {
  name                = "api"
  zone_name           = azurerm_private_dns_zone.private_zone.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["192.168.0.4"]
}

resource "azurerm_dns_a_record" "public_api" {
  name                = "api"
  zone_name           = azurerm_dns_zone.public_zone.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = ["13.92.173.1"]
}
```

**Explanation**:
1. **Provider Configuration**: Specifies the Azure provider.
2. **Resource Group**: Creates a resource group named `tailspintoys-rg` in the `Central US` region.
3. **Public DNS Zone**: Creates a public DNS zone named `tailspintoys.com`.
4. **Private DNS Zone**: Creates a private DNS zone named `internal.tailspintoys.com`.
5. **Internal A Record**: Creates an A record named `api` in the private DNS zone, pointing to the IP address `192.168.0.4`.
6. **Public A Record**: Creates an A record named `api` in the public DNS zone, pointing to the IP address `13.92.173.1`.

### Example 

5: Disaster Recovery and Failover

**Scenario**: Northwind Traders wants a robust disaster recovery solution for its critical applications.

**Terraform Script**:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg_primary" {
  name     = "northwind-primary-rg"
  location = "West US"
}

resource "azurerm_resource_group" "rg_secondary" {
  name     = "northwind-secondary-rg"
  location = "East US"
}

resource "azurerm_dns_zone" "primary_zone" {
  name                = "northwindtraders.com"
  resource_group_name = azurerm_resource_group.rg_primary.name
}

resource "azurerm_dns_zone" "secondary_zone" {
  name                = "northwindtraders.com"
  resource_group_name = azurerm_resource_group.rg_secondary.name
}

resource "azurerm_dns_a_record" "www_primary" {
  name                = "www"
  zone_name           = azurerm_dns_zone.primary_zone.name
  resource_group_name = azurerm_resource_group.rg_primary.name
  ttl                 = 300
  records             = ["10.0.0.1"]
}

resource "azurerm_dns_a_record" "www_secondary" {
  name                = "www"
  zone_name           = azurerm_dns_zone.secondary_zone.name
  resource_group_name = azurerm_resource_group.rg_secondary.name
  ttl                 = 300
  records             = ["10.0.1.1"]
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "northwind-tm-profile"
  resource_group_name = azurerm_resource_group.rg_primary.name
  location            = "global"

  dns_config {
    relative_name = "www"
    ttl           = 300
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  traffic_routing_method = "Priority"
}

resource "azurerm_traffic_manager_endpoint" "primary" {
  name                = "primary-endpoint"
  resource_group_name = azurerm_resource_group.rg_primary.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.primary_zone.id
  endpoint_location   = "West US"
  priority            = 1
}

resource "azurerm_traffic_manager_endpoint" "secondary" {
  name                = "secondary-endpoint"
  resource_group_name = azurerm_resource_group.rg_secondary.name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  type                = "azureEndpoints"

  target_resource_id  = azurerm_dns_zone.secondary_zone.id
  endpoint_location   = "East US"
  priority            = 2
}
```

**Explanation**:
1. **Provider Configuration**: Specifies the Azure provider.
2. **Primary Resource Group**: Creates a resource group named `northwind-primary-rg` in the `West US` region.
3. **Secondary Resource Group**: Creates a resource group named `northwind-secondary-rg` in the `East US` region.
4. **Primary DNS Zone**: Creates a primary DNS zone named `northwindtraders.com` in the primary resource group.
5. **Secondary DNS Zone**: Creates a secondary DNS zone named `northwindtraders.com` in the secondary resource group.
6. **Primary A Record**: Creates an A record named `www` in the primary DNS zone, pointing to the IP address `10.0.0.1`.
7. **Secondary A Record**: Creates an A record named `www` in the secondary DNS zone, pointing to the IP address `10.0.1.1`.
8. **Traffic Manager Profile**: Creates a Traffic Manager profile named `northwind-tm-profile` with a priority-based routing method. This profile prioritizes traffic to the primary endpoint.
9. **Primary Endpoint**: Creates a primary Traffic Manager endpoint in the `West US` region.
10. **Secondary Endpoint**: Creates a secondary Traffic Manager endpoint in the `East US` region.

These Terraform scripts provide a comprehensive setup for each scenario, leveraging Azure DNS, Traffic Manager, and other Azure services to meet specific requirements. Adjustments can be made based on the exact needs of your infrastructure and business logic.
