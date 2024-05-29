The Azure Well-Architected Framework is a set of guiding principles designed to help architects, developers, and IT professionals build high-quality cloud applications. It provides best practices and strategies to ensure that applications are optimized across several key pillars. The framework focuses on the following five pillars:

### 1. Cost Optimization
This pillar focuses on managing and optimizing costs to achieve business objectives while avoiding unnecessary expenses. Key practices include:
- **Cost Management:** Implementing tools like Azure Cost Management to monitor and control spending.
- **Right-Sizing:** Matching resource types and sizes to current demand to avoid over-provisioning.
- **Auto-Scaling:** Using Azure's auto-scaling capabilities to automatically adjust resources based on workload demands.
- **Reserved Instances and Spot Instances:** Leveraging Azure Reserved Instances for predictable workloads and Spot Instances for transient or fault-tolerant workloads to reduce costs.

### 2. Operational Excellence
Operational excellence involves running and monitoring systems to deliver business value and continually improving supporting processes and procedures. Key practices include:
- **Automation:** Automating deployment, configuration, and management tasks using tools like Azure DevOps and ARM templates.
- **Monitoring and Logging:** Implementing comprehensive monitoring and logging solutions using Azure Monitor, Log Analytics, and Application Insights.
- **Incident Response:** Establishing robust incident management and response procedures to quickly address and resolve issues.
- **Continuous Improvement:** Regularly reviewing and refining operational processes to enhance efficiency and effectiveness.

### 3. Performance Efficiency
This pillar focuses on ensuring applications are performant and can scale to meet user demands. Key practices include:
- **Performance Monitoring:** Using tools like Azure Monitor and Application Insights to track performance metrics and identify bottlenecks.
- **Scaling Strategies:** Implementing horizontal and vertical scaling strategies to handle varying loads.
- **Caching and Content Delivery:** Utilizing Azure Cache for Redis and Azure Content Delivery Network (CDN) to reduce latency and improve response times.
- **Optimization:** Continuously optimizing applications and infrastructure for better performance.

### 4. Reliability
Reliability ensures that applications can recover from failures and continue to function as intended. Key practices include:
- **Redundancy and Replication:** Implementing redundancy and data replication strategies using Azure Availability Zones and Geo-Replication.
- **Backup and Disaster Recovery:** Establishing comprehensive backup and disaster recovery plans with services like Azure Backup and Azure Site Recovery.
- **Health Monitoring:** Continuously monitoring the health of applications and infrastructure using Azure Monitor and Azure Service Health.
- **Failover and Resiliency:** Designing applications to automatically failover and recover from unexpected issues.

### 5. Security
Security involves protecting applications and data from threats. Key practices include:
- **Identity and Access Management:** Using Azure Active Directory (Azure AD) for secure identity and access management.
- **Data Protection:** Encrypting data at rest and in transit using Azure Key Vault and Azure Disk Encryption.
- **Network Security:** Implementing network security measures such as Network Security Groups (NSGs), Azure Firewall, and Azure DDoS Protection.
- **Compliance:** Ensuring applications meet industry and regulatory compliance requirements through tools like Azure Policy and Azure Blueprints.

### Implementation Tools and Services
Azure offers various tools and services to implement the principles of the Well-Architected Framework:
- **Azure Advisor:** Provides personalized best practices and recommendations to optimize your Azure deployments.
- **Azure Well-Architected Review:** An assessment tool that helps evaluate workloads against the framework's pillars.
- **Azure DevOps:** Supports continuous integration, continuous delivery, and automation.
- **Azure Monitor and Application Insights:** Provide comprehensive monitoring and diagnostics capabilities.
- **Azure Security Center:** Enhances security posture through advanced threat protection.

### Conclusion
The Azure Well-Architected Framework is a comprehensive guide to building and maintaining high-quality applications on Azure. By adhering to its principles and utilizing Azure’s robust tools and services, organizations can achieve greater efficiency, reliability, performance, and security while optimizing costs.


Here are some real-world examples that illustrate the application of the Azure Well-Architected Framework across its five pillars:

### 1. Cost Optimization: Contoso Retail
**Scenario:** Contoso Retail, an e-commerce company, experienced fluctuating traffic with peak loads during sales events.
**Solution:** 
- **Auto-Scaling:** Contoso implemented auto-scaling for their virtual machines and Azure App Services to automatically adjust the number of instances based on real-time traffic.
- **Reserved Instances:** They purchased Azure Reserved Instances for their steady-state workloads to reduce costs.
- **Cost Management:** Using Azure Cost Management, they monitored and analyzed their cloud spend, setting up alerts for unexpected spikes.

**Outcome:** Contoso reduced their overall cloud spend by 30% while ensuring they could handle peak loads without manual intervention.

### 2. Operational Excellence: Fabrikam Insurance
**Scenario:** Fabrikam Insurance needed to ensure continuous deployment and minimize downtime for their critical insurance applications.
**Solution:**
- **Automation:** They adopted Azure DevOps for CI/CD pipelines, automating the deployment process for new features and updates.
- **Monitoring and Logging:** Implemented Azure Monitor and Log Analytics to gain insights into application performance and operational health.
- **Incident Response:** Established automated alerting and a robust incident response process to quickly address issues.

**Outcome:** Fabrikam improved deployment frequency by 50% and reduced mean time to recovery (MTTR) by 40%.

### 3. Performance Efficiency: Tailwind Traders
**Scenario:** Tailwind Traders, a global supply chain company, needed to improve the performance of their inventory management system.
**Solution:**
- **Caching:** Implemented Azure Cache for Redis to cache frequently accessed data, reducing database load and improving response times.
- **Content Delivery:** Used Azure Content Delivery Network (CDN) to distribute content globally, ensuring fast load times for users in different regions.
- **Performance Monitoring:** Employed Application Insights to monitor performance metrics and identify bottlenecks.

**Outcome:** Tailwind Traders achieved a 60% reduction in page load times and improved overall application responsiveness.

### 4. Reliability: Adventure Works
**Scenario:** Adventure Works, a manufacturer of outdoor equipment, needed to ensure high availability and disaster recovery for their ERP system.
**Solution:**
- **Redundancy:** Deployed their application across multiple Azure Availability Zones to ensure high availability.
- **Disaster Recovery:** Implemented Azure Site Recovery for seamless disaster recovery and conducted regular failover tests.
- **Health Monitoring:** Used Azure Service Health to monitor the health of their services and set up automated failover processes.

**Outcome:** Adventure Works achieved a 99.99% uptime and reduced potential downtime impact with a robust disaster recovery strategy.

### 5. Security: Northwind Traders
**Scenario:** Northwind Traders, a global trading company, needed to secure sensitive customer data and comply with GDPR.
**Solution:**
- **Identity Management:** Used Azure Active Directory (Azure AD) for single sign-on (SSO) and multi-factor authentication (MFA) to secure user access.
- **Data Protection:** Encrypted data at rest using Azure Disk Encryption and data in transit with SSL/TLS.
- **Network Security:** Implemented Azure Firewall, Network Security Groups (NSGs), and Azure DDoS Protection to secure their network perimeter.
- **Compliance:** Utilized Azure Policy and Azure Blueprints to ensure compliance with GDPR and other regulatory requirements.

**Outcome:** Northwind Traders enhanced their security posture, achieving compliance with GDPR and significantly reducing the risk of data breaches.

These examples demonstrate how different organizations have successfully applied the Azure Well-Architected Framework to optimize costs, improve operational excellence, enhance performance efficiency, ensure reliability, and bolster security.

Below are detailed Terraform scripts for each of the real-world examples provided. These scripts will help you implement the various solutions on Azure.

### 1. Cost Optimization: Contoso Retail

**Auto-Scaling for Azure App Service**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "contoso-retail-rg"
  location = "East US"
}

resource "azurerm_app_service_plan" "asp" {
  name                = "contoso-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = "Standard"
    size = "S1"
  }
  maximum_elastic_worker_count = 10
}

resource "azurerm_app_service" "app" {
  name                = "contoso-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.asp.id

  site_config {
    always_on = true
  }
}

resource "azurerm_monitor_autoscale_setting" "autoscale" {
  name                = "contoso-autoscale"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  target_resource_id  = azurerm_app_service_plan.asp.id

  profile {
    name = "defaultProfile"
    capacity {
      minimum = "1"
      maximum = "10"
      default = "1"
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.asp.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 70
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT1M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.asp.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 30
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT1M"
      }
    }
  }
}
```

### 2. Operational Excellence: Fabrikam Insurance

**Azure DevOps Pipeline for CI/CD**

This script assumes you have a project in Azure DevOps and a repository set up. The pipeline file `azure-pipelines.yml` is committed to your repository.

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

steps:
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '5.x'
    installationPath: $(Agent.ToolsDirectory)/dotnet

- script: |
    dotnet build --configuration $(buildConfiguration)
  displayName: 'Build'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'

- task: AzureRmWebAppDeployment@4
  inputs:
    azureSubscription: '<Azure Service Connection>'
    appType: 'webApp'
    WebAppName: '<Your Web App Name>'
    package: '$(Build.ArtifactStagingDirectory)/drop'
```

### 3. Performance Efficiency: Tailwind Traders

**Azure Cache for Redis and CDN**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "tailwind-traders-rg"
  location = "West US"
}

resource "azurerm_redis_cache" "redis" {
  name                = "tailwind-redis"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  capacity            = 1
  family              = "C"
  sku_name            = "Basic"
}

resource "azurerm_cdn_profile" "cdn_profile" {
  name                = "tailwind-cdn-profile"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard_Microsoft"
}

resource "azurerm_cdn_endpoint" "cdn_endpoint" {
  name                = "tailwind-cdn-endpoint"
  resource_group_name = azurerm_resource_group.rg.name
  profile_name        = azurerm_cdn_profile.cdn_profile.name
  location            = azurerm_resource_group.rg.location
  origins {
    name      = "origin-storage"
    host_name = "your-storage-account.blob.core.windows.net"
  }
}
```

### 4. Reliability: Adventure Works

**Availability Zones and Disaster Recovery with Site Recovery**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "adventure-works-rg"
  location = "Central US"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "adventure-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "public_ip" {
  name                = "adventure-public-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  zones               = ["1", "2", "3"]
}

resource "azurerm_network_interface" "nic" {
  name                = "adventure-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

resource "azurerm_virtual_machine" "vm" {
  name                  = "adventure-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_DS1_v2"
  availability_set_id   = azurerm_availability_set.avset.id

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                = "adventure-replication-policy"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  replication_frequency_in_seconds = 30
  recovery_point_retention_in_hours = 24
  app_consistent_snapshot_frequency_in_hours = 4
}

resource "azurerm_site_recovery_protection_container_mapping" "mapping" {
  name                = "adventure-mapping"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  source_protection_container_id = azurerm_site_recovery_protection_container.source.id
  target_protection_container_id = azurerm_site_recovery_protection_container.target.id
  policy_id = azurerm_site_recovery_replication_policy.policy.id
}
```

### 5. Security: Northwind Traders

**Azure Active Directory and Network Security**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "northwind-traders-rg"
  location = "North Europe"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "northwind-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm

_resource_group.rg.name
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_network_security_group" "nsg" {
  name                = "northwind-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "AllowSSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface" "nic" {
  name                = "northwind-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }

  network_security_group_id = azurerm_network_security_group.nsg.id
}

resource "azurerm_virtual_machine" "vm" {
  name                  = "northwind-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_B1ms"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}

resource "azurerm_key_vault" "kv" {
  name                = "northwind-kv"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = ["get", "list"]
    secret_permissions = ["get", "list"]
    certificate_permissions = ["get", "list"]
  }
}

resource "azurerm_active_directory_domain_service" "adds" {
  name                = "northwind-adds"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  domain_name         = "northwindtraders.com"
  sku                 = "standard"
}
```

These Terraform scripts provide a starting point for implementing the solutions described in the real-world examples. Modify them according to your specific requirements and environment.


Sure! Let's go through each of the Terraform scripts in detail.

### 1. Cost Optimization: Contoso Retail

#### Auto-Scaling for Azure App Service

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "contoso-retail-rg"
  location = "East US"
}
```
- **Provider Configuration**: The `azurerm` provider is configured to interact with Azure.
- **Resource Group**: Creates a resource group named `contoso-retail-rg` in the `East US` region.

```hcl
resource "azurerm_app_service_plan" "asp" {
  name                = "contoso-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = "Standard"
    size = "S1"
  }
  maximum_elastic_worker_count = 10
}
```
- **App Service Plan**: Defines an App Service Plan named `contoso-asp` in the resource group. It uses the `Standard` tier with a `S1` size, and sets the maximum elastic worker count to 10 for auto-scaling.

```hcl
resource "azurerm_app_service" "app" {
  name                = "contoso-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.asp.id

  site_config {
    always_on = true
  }
}
```
- **App Service**: Creates an App Service named `contoso-app` in the same resource group, linked to the App Service Plan. The `always_on` setting is enabled to keep the app awake.

```hcl
resource "azurerm_monitor_autoscale_setting" "autoscale" {
  name                = "contoso-autoscale"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  target_resource_id  = azurerm_app_service_plan.asp.id

  profile {
    name = "defaultProfile"
    capacity {
      minimum = "1"
      maximum = "10"
      default = "1"
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.asp.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 70
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT1M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.asp.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 30
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT1M"
      }
    }
  }
}
```
- **Auto-Scaling Settings**: Configures auto-scaling for the App Service Plan.
  - **Profile**: Defines the default scaling profile.
  - **Capacity**: Sets the minimum, maximum, and default instance counts.
  - **Scaling Rules**: 
    - **Increase Instances**: If CPU percentage exceeds 70% for 5 minutes, it scales up by one instance.
    - **Decrease Instances**: If CPU percentage is below 30% for 5 minutes, it scales down by one instance.

### 2. Operational Excellence: Fabrikam Insurance

#### Azure DevOps Pipeline for CI/CD

This YAML script is placed in the repository to define the CI/CD pipeline.

```yaml
trigger:
- main
```
- **Trigger**: Specifies that the pipeline should run on every push to the `main` branch.

```yaml
pool:
  vmImage: 'ubuntu-latest'
```
- **Pool**: Specifies the use of the latest Ubuntu image for running the pipeline.

```yaml
variables:
  buildConfiguration: 'Release'
```
- **Variables**: Defines a variable for the build configuration, set to `Release`.

```yaml
steps:
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '5.x'
    installationPath: $(Agent.ToolsDirectory)/dotnet
```
- **UseDotNet Task**: Installs the .NET SDK version 5.x.

```yaml
- script: |
    dotnet build --configuration $(buildConfiguration)
  displayName: 'Build'
```
- **Build Step**: Runs the `dotnet build` command with the specified configuration.

```yaml
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'
```
- **Publish Build Artifacts**: Publishes the build output to the Azure DevOps artifacts.

```yaml
- task: AzureRmWebAppDeployment@4
  inputs:
    azureSubscription: '<Azure Service Connection>'
    appType: 'webApp'
    WebAppName: '<Your Web App Name>'
    package: '$(Build.ArtifactStagingDirectory)/drop'
```
- **Deploy to Azure Web App**: Deploys the build artifacts to an Azure Web App using a predefined Azure service connection.

### 3. Performance Efficiency: Tailwind Traders

#### Azure Cache for Redis and CDN

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "tailwind-traders-rg"
  location = "West US"
}
```
- **Provider Configuration**: The `azurerm` provider is configured to interact with Azure.
- **Resource Group**: Creates a resource group named `tailwind-traders-rg` in the `West US` region.

```hcl
resource "azurerm_redis_cache" "redis" {
  name                = "tailwind-redis"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  capacity            = 1
  family              = "C"
  sku_name            = "Basic"
}
```
- **Redis Cache**: Creates an Azure Redis Cache instance named `tailwind-redis` with a `Basic` SKU and capacity of 1.

```hcl
resource "azurerm_cdn_profile" "cdn_profile" {
  name                = "tailwind-cdn-profile"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard_Microsoft"
}
```
- **CDN Profile**: Creates a CDN profile named `tailwind-cdn-profile` using the `Standard_Microsoft` SKU.

```hcl
resource "azurerm_cdn_endpoint" "cdn_endpoint" {
  name                = "tailwind-cdn-endpoint"
  resource_group_name = azurerm_resource_group.rg.name
  profile_name        = azurerm_cdn_profile.cdn_profile.name
  location            = azurerm_resource_group.rg.location
  origins {
    name      = "origin-storage"
    host_name = "your-storage-account.blob.core.windows.net"
  }
}
```
- **CDN Endpoint**: Creates a CDN endpoint named `tailwind-cdn-endpoint`, pointing to a storage account origin.

### 4. Reliability: Adventure Works

#### Availability Zones and Disaster Recovery with Site Recovery

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "adventure-works-rg"
  location = "Central US"
}
```
- **Provider Configuration**: The `azurerm` provider is configured to interact with Azure.
- **Resource Group**: Creates a resource group named `adventure-works-rg` in the `Central US` region.

```hcl
resource "azurerm_virtual_network" "vnet" {
  name                = "adventure-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}
```
- **Virtual Network**: Creates a virtual network named `adventure-vnet` with a specified address space.
- **Subnet**: Defines a subnet within the virtual network.

```hcl
resource "azurerm_public_ip" "public_ip" {
  name                = "adventure-public-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"


  zones               = ["1", "2", "3"]
}
```
- **Public IP Address**: Creates a static public IP address with availability across three zones.

```hcl
resource "azurerm_network_interface" "nic" {
  name                = "adventure-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}
```
- **Network Interface**: Creates a network interface linked to the subnet and public IP address.

```hcl
resource "azurerm_virtual_machine" "vm" {
  name                  = "adventure-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_DS1_v2"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}
```
- **Virtual Machine**: Creates a VM named `adventure-vm` with a specified VM size, image reference, and OS configuration.

```hcl
resource "azurerm_site_recovery_replication_policy" "policy" {
  name                = "adventure-replication-policy"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  replication_frequency_in_seconds = 30
  recovery_point_retention_in_hours = 24
  app_consistent_snapshot_frequency_in_hours = 4
}
```
- **Replication Policy**: Creates a site recovery replication policy with specified parameters for replication frequency, recovery point retention, and snapshot frequency.

```hcl
resource "azurerm_site_recovery_protection_container_mapping" "mapping" {
  name                = "adventure-mapping"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  source_protection_container_id = azurerm_site_recovery_protection_container.source.id
  target_protection_container_id = azurerm_site_recovery_protection_container.target.id
  policy_id = azurerm_site_recovery_replication_policy.policy.id
}
```
- **Protection Container Mapping**: Maps the source and target protection containers using the replication policy.

### 5. Security: Northwind Traders

#### Azure Active Directory and Network Security

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "northwind-traders-rg"
  location = "North Europe"
}
```
- **Provider Configuration**: The `azurerm` provider is configured to interact with Azure.
- **Resource Group**: Creates a resource group named `northwind-traders-rg` in the `North Europe` region.

```hcl
resource "azurerm_virtual_network" "vnet" {
  name                = "northwind-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.1.1.0/24"]
}
```
- **Virtual Network**: Creates a virtual network named `northwind-vnet` with a specified address space.
- **Subnet**: Defines a subnet within the virtual network.

```hcl
resource "azurerm_network_security_group" "nsg" {
  name                = "northwind-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "AllowSSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
```
- **Network Security Group**: Creates a network security group named `northwind-nsg` with a rule to allow SSH traffic on port 22.

```hcl
resource "azurerm_network_interface" "nic" {
  name                = "northwind-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }

  network_security_group_id = azurerm_network_security_group.nsg.id
}
```
- **Network Interface**: Creates a network interface linked to the subnet, public IP address, and network security group.

```hcl
resource "azurerm_virtual_machine" "vm" {
  name                  = "northwind-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_B1ms"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "adminuser"
    admin_password = "Password1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}
```
- **Virtual Machine**: Creates a VM named `northwind-vm` with a specified VM size, image reference, and OS configuration.

```hcl
resource "azurerm_key_vault" "kv" {
  name                = "northwind-kv"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = ["get", "list"]
    secret_permissions = ["get", "list"]
    certificate_permissions = ["get", "list"]
  }
}
```
- **Key Vault**: Creates a Key Vault named `northwind-kv` with specified access policies.

```hcl
resource "azurerm_active_directory_domain_service" "adds" {
  name                = "northwind-adds"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  domain_name         = "northwindtraders.com"
  sku                 = "standard"
}
```
- **Active Directory Domain Service**: Creates an Active Directory Domain Service for the domain `northwindtraders.com` with a `standard` SKU.

These detailed explanations should help you understand how the Terraform scripts work and how they can be modified to suit specific needs. If you have further questions or need additional details, feel free to ask!
