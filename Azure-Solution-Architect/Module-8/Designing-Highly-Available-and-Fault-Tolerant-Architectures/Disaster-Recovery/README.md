Designing highly available and fault-tolerant architectures in Azure involves ensuring that your application can withstand failures and continue to operate with minimal disruption. Here’s a comprehensive guide on how to achieve this:

### 1. **Understand High Availability (HA) and Fault Tolerance (FT)**

- **High Availability (HA):** Ensuring that the application is available for use most of the time, with minimal downtime.
- **Fault Tolerance (FT):** The ability of the system to continue functioning even when part of it fails.

### 2. **Azure Regions and Availability Zones**

- **Regions:** Azure data centers are grouped into regions across the globe. Choosing the right region is crucial for latency and compliance.
- **Availability Zones:** Each region may have multiple availability zones (AZs), which are physically separate locations within a region. Distributing your resources across multiple AZs can enhance availability.

### 3. **Resource Redundancy**

- **Virtual Machines (VMs):** Use availability sets and availability zones to distribute VMs across multiple fault and update domains.
- **Managed Disks:** Use premium SSDs and ultra disks for higher performance and reliability.
- **Scale Sets:** Automatically scale your VM instances to handle load increases and distribute them across fault domains.

### 4. **Load Balancing**

- **Azure Load Balancer:** Distributes incoming traffic across multiple VMs in the same region.
- **Traffic Manager:** DNS-based load balancer that enables distribution of traffic across multiple regions.
- **Application Gateway:** Provides application-level load balancing and web application firewall (WAF) capabilities.

### 5. **Data Redundancy and Replication**

- **Azure Storage:** Use geo-redundant storage (GRS) or read-access geo-redundant storage (RA-GRS) to replicate data to a secondary region.
- **SQL Database:** Use active geo-replication for automatic failover of databases.
- **Cosmos DB:** Globally distributed database that replicates data across multiple regions.

### 6. **Disaster Recovery**

- **Azure Site Recovery:** Automates the replication of VMs to a secondary region and orchestrates failover and failback.
- **Backup Services:** Regularly back up data and VMs using Azure Backup to ensure data integrity and quick recovery.

### 7. **Networking Resilience**

- **Virtual Networks (VNet):** Design virtual networks with redundancy and failover capabilities.
- **VPN Gateway:** Use redundant VPN gateways in different regions for site-to-site VPN.
- **ExpressRoute:** Provides dedicated private connectivity, with redundancy options for critical applications.

### 8. **Monitoring and Management**

- **Azure Monitor:** Provides insights and analytics on the performance and health of your resources.
- **Azure Service Health:** Notifies you of service issues and planned maintenance that might affect your resources.
- **Log Analytics:** Centralized repository for collecting and analyzing log data from various sources.

### 9. **Design Patterns**

- **Circuit Breaker:** Prevents system overload by managing failed calls and retries.
- **Retry Pattern:** Implements logic to handle transient failures by retrying failed operations.
- **Health Endpoint Monitoring:** Regularly checks the health of application components to ensure they are functioning properly.

### 10. **Best Practices**

- **Deploy across multiple regions:** To ensure geo-redundancy and quick failover.
- **Automate failover processes:** Using Azure Site Recovery and Traffic Manager.
- **Regularly test disaster recovery plans:** Ensure that the failover mechanisms and backups work as expected.
- **Design for scalability:** Use Azure services that can scale automatically based on demand.
- **Implement security best practices:** Protect data and applications to maintain integrity and availability.

### Example Architecture

A typical highly available and fault-tolerant architecture might include:

- **Web Tier:** Deployed across multiple availability zones with an Azure Load Balancer.
- **Application Tier:** Use VM Scale Sets for scalability and distribution across fault domains.
- **Database Tier:** Use Azure SQL Database with active geo-replication.
- **Data Storage:** Use Azure Blob Storage with RA-GRS.
- **Networking:** Use Azure Traffic Manager for global load balancing and Azure VPN Gateway for secure connections.

By following these guidelines and leveraging Azure’s robust suite of services, you can design architectures that are both highly available and fault-tolerant, ensuring continuous operation and minimal downtime for your applications.

Disaster Recovery (DR) in Azure involves preparing for, responding to, and recovering from potential service interruptions, ranging from minor disruptions to catastrophic events. Azure provides several services and strategies to ensure business continuity and minimize downtime. Here’s a detailed guide on implementing disaster recovery in Azure:

### 1. **Understanding Disaster Recovery**

Disaster Recovery is part of a broader Business Continuity Plan (BCP) and focuses on restoring critical IT systems, data, and operations following a disruption. Key components include:
- **Recovery Time Objective (RTO):** The maximum acceptable time that a system can be offline.
- **Recovery Point Objective (RPO):** The maximum acceptable amount of data loss measured in time.

### 2. **Azure Site Recovery (ASR)**

Azure Site Recovery (ASR) is a primary service for orchestrating disaster recovery for on-premises and Azure VMs.

#### Key Features:
- **Replication:** Continuous replication of VMs to a secondary Azure region.
- **Failover and Failback:** Automated failover to the secondary region and seamless failback to the primary site.
- **Customizable Recovery Plans:** Define specific steps for failover and failback, including scripts and manual interventions.

#### Implementation Steps:
1. **Set Up Recovery Services Vault:** Create a Recovery Services Vault in the Azure portal.
2. **Configure Replication Settings:** Choose source and target regions, specify VM replication policies, and configure storage accounts.
3. **Enable Replication:** Start the replication process for your VMs or physical servers.
4. **Create Recovery Plans:** Define recovery plans with steps and actions for failover and failback.
5. **Test Failover:** Perform test failovers to validate the DR plan without affecting production workloads.
6. **Initiate Failover:** In the event of a disaster, initiate a planned or unplanned failover.
7. **Perform Failback:** After resolving the issue, initiate failback to the primary region.

### 3. **Backup Services**

Azure Backup provides reliable and secure backup solutions for VMs, databases, and other resources.

#### Key Features:
- **Automated Backups:** Schedule backups with retention policies.
- **Geo-Redundancy:** Store backups in geo-redundant storage to ensure data availability.
- **Point-in-Time Restore:** Restore data from specific points in time.

#### Implementation Steps:
1. **Set Up Backup Policy:** Define backup schedules and retention policies in the Azure portal.
2. **Enable Backups:** Select the resources to back up and apply the backup policy.
3. **Monitor Backups:** Use Azure Monitor to track backup status and alerts.
4. **Restore Data:** In the event of data loss, restore data from backups using the Azure portal.

### 4. **Geo-Redundancy for Databases**

For databases, Azure offers geo-replication options to ensure high availability and disaster recovery.

#### SQL Database:
- **Active Geo-Replication:** Create readable secondary replicas in different regions. In the event of a primary region failure, you can failover to the secondary replica.
- **Auto-Failover Groups:** Automate failover for a group of databases.

#### Cosmos DB:
- **Global Distribution:** Automatically replicate data across multiple regions, providing high availability and low-latency access.
- **Multi-Region Writes:** Enable multi-region writes to ensure data availability even during regional failures.

### 5. **Networking Resilience**

- **Azure Traffic Manager:** Distributes traffic across multiple regions, providing automatic failover in case of regional outages.
- **VPN Gateway and ExpressRoute:** Use redundant connections to ensure network connectivity during outages.

### 6. **Implementing Best Practices**

#### Regular Testing:
- **Conduct Regular DR Drills:** Simulate disaster scenarios to test the effectiveness of your DR plan.
- **Update and Review Plans:** Periodically review and update your DR plans based on changing business needs and technology updates.

#### Data Protection:
- **Use Encryption:** Ensure data is encrypted in transit and at rest to protect against data breaches.
- **Access Controls:** Implement strict access controls and identity management to secure access to your DR infrastructure.

#### Documentation:
- **Maintain Detailed Documentation:** Document all DR processes, including recovery steps, responsible personnel, and contact information.
- **Train Staff:** Ensure all relevant staff are trained on DR procedures and know their roles during a disaster.

### 7. **Example Disaster Recovery Architecture**

A comprehensive DR architecture might include:
- **Primary Site:** Located in a specific Azure region, hosting production workloads.
- **Secondary Site:** Located in a different Azure region, configured for ASR replication.
- **Backup Services:** Regular backups stored in geo-redundant storage.
- **Database Geo-Replication:** Active geo-replication for SQL Database and Cosmos DB.
- **Traffic Manager:** Configured to route traffic to the secondary site in case of a primary site failure.
- **Monitoring and Alerts:** Azure Monitor and Log Analytics configured to detect and alert on potential issues.

By leveraging these Azure services and best practices, you can create a robust disaster recovery plan that ensures business continuity and minimizes the impact of disruptions.


Sure, here are some real-world examples of disaster recovery implementations in Azure across different industries:

### 1. **Healthcare: Contoso Hospital**

**Scenario:**
Contoso Hospital relies on critical applications for patient management, electronic health records (EHR), and medical imaging. Ensuring these systems are always available is crucial for patient care.

**Implementation:**
- **Azure Site Recovery (ASR):** Contoso Hospital replicates their on-premises servers and VMs to Azure using ASR. This ensures that in the event of an on-premises failure, operations can continue from the Azure environment.
- **Azure Backup:** Regular backups of EHR and patient data are stored in geo-redundant storage to ensure data protection and quick recovery.
- **SQL Database Geo-Replication:** The hospital's SQL databases are configured with active geo-replication, allowing instant failover to a secondary region in case of a primary region outage.

**Benefits:**
- Ensured patient data is always accessible.
- Minimized downtime for critical healthcare applications.
- Quick and automated failover to secondary regions.

### 2. **Financial Services: Fabrikam Bank**

**Scenario:**
Fabrikam Bank requires high availability and disaster recovery solutions to ensure the availability of its online banking platform and transaction processing systems.

**Implementation:**
- **Azure Traffic Manager:** Used to distribute traffic across multiple regions. In the event of a regional outage, traffic is automatically routed to a healthy region.
- **Active Geo-Replication for SQL Database:** Critical transactional databases are replicated across multiple regions. This ensures that transactions can continue without interruption even if one region fails.
- **Azure Site Recovery:** The bank's VMs running the online banking application are replicated to a secondary region. In case of a disaster, failover can be initiated quickly to restore services.

**Benefits:**
- High availability for online banking services.
- Continuous availability of transaction processing.
- Reduced risk of data loss and downtime.

### 3. **Retail: Northwind Traders**

**Scenario:**
Northwind Traders operates an e-commerce platform that must be available 24/7 to handle customer orders and inventory management.

**Implementation:**
- **Azure Traffic Manager and Azure Front Door:** Used for global load balancing and application acceleration. Traffic is routed to the nearest available region, ensuring low latency and high availability.
- **Cosmos DB Global Distribution:** The e-commerce platform uses Cosmos DB for its product catalog and customer data. Data is replicated across multiple regions to ensure it is always available.
- **Azure Backup:** Daily backups of customer orders and inventory data are stored in geo-redundant storage.

**Benefits:**
- Improved customer experience with low-latency access.
- High availability of critical e-commerce services.
- Ensured data protection and quick recovery in case of issues.

### 4. **Manufacturing: Contoso Manufacturing**

**Scenario:**
Contoso Manufacturing uses IoT devices and data analytics for real-time monitoring of their production lines. They need to ensure this system is always operational to avoid costly downtime.

**Implementation:**
- **Azure IoT Hub and IoT Edge:** IoT devices send data to Azure IoT Hub, which is set up with disaster recovery configurations. IoT Edge devices provide local processing to ensure operations continue even if connectivity to the cloud is temporarily lost.
- **Azure Site Recovery:** The on-premises servers running data analytics applications are replicated to Azure. In case of on-premises failure, these applications can be run from the cloud.
- **Azure Monitor and Alerts:** Real-time monitoring of IoT devices and analytics applications. Alerts are set up for any anomalies, allowing quick response to potential issues.

**Benefits:**
- Continuous monitoring and operation of production lines.
- Quick failover to Azure in case of on-premises issues.
- Minimized downtime and production losses.

### 5. **Public Sector: City Government**

**Scenario:**
A city government relies on several web applications to provide services to citizens, including permit processing, public records access, and emergency services.

**Implementation:**
- **Azure Government Cloud:** The city uses Azure Government for compliance with regulatory requirements. Critical applications are hosted in Azure Government regions.
- **Azure Site Recovery:** The city’s applications are replicated to a secondary Azure Government region to ensure continuity in case of a primary region failure.
- **Active Geo-Replication for Azure SQL Database:** Public records and permit databases are geo-replicated to ensure they are always accessible.

**Benefits:**
- Ensured availability of critical public services.
- Compliance with regulatory requirements for data security and privacy.
- Quick recovery from regional outages or disasters.

These examples illustrate how organizations across different industries leverage Azure’s disaster recovery services to ensure business continuity, protect critical data, and minimize downtime during unexpected events.


Here are simplified Terraform scripts for the disaster recovery setups in each real-world example. These scripts provide basic configurations and should be tailored to fit the specific needs and infrastructure of each organization.

### 1. **Healthcare: Contoso Hospital**

**Scenario: Azure Site Recovery and SQL Database Geo-Replication**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "ContosoHospitalRG"
  location = "West US"
}

resource "azurerm_recovery_services_vault" "vault" {
  name                = "ContosoRecoveryVault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                 = "ContosoReplicationPolicy"
  resource_group_name  = azurerm_resource_group.rg.name
  recovery_vault_name  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes = 1440
  application_consistent_snapshot_frequency_in_minutes = 60
}

resource "azurerm_sql_server" "sql" {
  name                         = "contososqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "ContosoEHRDB"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql.name
  sku_name            = "S1"
}

resource "azurerm_sql_failover_group" "failover_group" {
  name                = "ContosoFailoverGroup"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.sql.name
  databases           = [azurerm_sql_database.sql_db.id]

  partner_servers {
    id = azurerm_sql_server.sql.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 5
  }
}
```

### 2. **Financial Services: Fabrikam Bank**

**Scenario: Azure Traffic Manager and SQL Database Geo-Replication**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "FabrikamBankRG"
  location = "East US"
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "FabrikamTrafficManager"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  traffic_routing_method = "Priority"

  dns_config {
    relative_name = "fabrikam"
    ttl           = 30
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  endpoint {
    name                = "Primary"
    target_resource_id  = azurerm_app_service.appservice.id
    endpoint_location   = azurerm_resource_group.rg.location
    priority            = 1
  }

  endpoint {
    name                = "Secondary"
    target_resource_id  = azurerm_app_service.appservice_secondary.id
    endpoint_location   = azurerm_resource_group.rg_secondary.location
    priority            = 2
  }
}

resource "azurerm_sql_server" "sql_primary" {
  name                         = "fabrikamprimarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_server" "sql_secondary" {
  name                         = "fabrikamsecondarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = "West US"
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "FabrikamDB"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql_primary.name
  sku_name            = "S1"
}

resource "azurerm_sql_failover_group" "failover_group" {
  name                = "FabrikamFailoverGroup"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.sql_primary.name
  databases           = [azurerm_sql_database.sql_db.id]

  partner_servers {
    id = azurerm_sql_server.sql_secondary.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 5
  }
}
```

### 3. **Retail: Northwind Traders**

**Scenario: Azure Traffic Manager, Cosmos DB Global Distribution, and Azure Backup**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "NorthwindTradersRG"
  location = "Central US"
}

resource "azurerm_cosmosdb_account" "cosmosdb" {
  name                = "northwindcosmosdb"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = "East US"
    failover_priority = 0
  }

  geo_location {
    location          = "West US"
    failover_priority = 1
  }
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "NorthwindTrafficManager"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  traffic_routing_method = "Priority"

  dns_config {
    relative_name = "northwind"
    ttl           = 30
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  endpoint {
    name                = "Primary"
    target_resource_id  = azurerm_app_service.appservice.id
    endpoint_location   = azurerm_resource_group.rg.location
    priority            = 1
  }

  endpoint {
    name                = "Secondary"
    target_resource_id  = azurerm_app_service.appservice_secondary.id
    endpoint_location   = azurerm_resource_group.rg_secondary.location
    priority            = 2
  }
}

resource "azurerm_backup_policy_vm" "backup_policy" {
  name                = "NorthwindBackupPolicy"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_backup_vault.vault.name

  backup {
    frequency = "Daily"
    time      = "02:00"
  }

  retention_daily {
    count = 7
  }
}

resource "azurerm_backup_protected_vm" "protected_vm" {
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_backup_vault.vault.name
  source_vm_id        = azurerm_windows_virtual_machine.vm.id
  backup_policy_id    = azurerm_backup_policy_vm.backup_policy.id
}
```

### 4. **Manufacturing: Contoso Manufacturing**

**Scenario: Azure IoT Hub, Azure Site Recovery, and Azure Monitor**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "ContosoManufacturingRG"
  location = "West Europe"
}

resource "azurerm_iothub" "iothub" {
  name                = "ContosoIoTHub"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku {
    name     = "S1"
    capacity = 1
  }
  retention_days = 7
}

resource "azurerm_recovery_services_vault" "vault" {
  name                = "ContosoRecoveryVault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                 = "ContosoReplicationPolicy"
  resource_group_name  = azurerm_resource_group.rg.name
  recovery_vault_name  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes = 1440
  application_consistent_snapshot_frequency_in_minutes = 60
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                =

 "ContosoLogAnalytics"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
}

resource "azurerm_monitor_diagnostic_setting" "iot_diagnostics" {
  name               = "IoTHubDiagnostics"
  target_resource_id = azurerm_iothub.iothub.id

  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id

  log {
    category = "Connections"
    enabled  = true
  }

  log {
    category = "DeviceTelemetry"
    enabled  = true
  }

  log {
    category = "Routes"
    enabled  = true
  }

  log {
    category = "TwinUpdates"
    enabled  = true
  }
}
```

### 5. **Public Sector: City Government**

**Scenario: Azure Government Cloud, Azure Site Recovery, and SQL Database Geo-Replication**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "CityGovRG"
  location = "US Gov Virginia"
}

resource "azurerm_recovery_services_vault" "vault" {
  name                = "CityGovRecoveryVault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                 = "CityGovReplicationPolicy"
  resource_group_name  = azurerm_resource_group.rg.name
  recovery_vault_name  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes = 1440
  application_consistent_snapshot_frequency_in_minutes = 60
}

resource "azurerm_sql_server" "sql_primary" {
  name                         = "citygovprimarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_server" "sql_secondary" {
  name                         = "citygovsecondarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = "US Gov Texas"
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "CityGovDB"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql_primary.name
  sku_name            = "S1"
}

resource "azurerm_sql_failover_group" "failover_group" {
  name                = "CityGovFailoverGroup"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.sql_primary.name
  databases           = [azurerm_sql_database.sql_db.id]

  partner_servers {
    id = azurerm_sql_server.sql_secondary.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 5
  }
}
```

These scripts provide a starting point for deploying disaster recovery solutions in Azure. You will need to customize them according to your specific requirements, such as the number of VMs, specific configurations, network settings, and compliance requirements.


Certainly! Let's dive into each Terraform script in detail, explaining the purpose and configuration of each resource.

### 1. **Healthcare: Contoso Hospital**

**Scenario: Azure Site Recovery and SQL Database Geo-Replication**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "ContosoHospitalRG"
  location = "West US"
}
```
- **provider "azurerm"**: Specifies the Azure provider for Terraform.
- **azurerm_resource_group "rg"**: Creates a resource group in the "West US" region named "ContosoHospitalRG".

```hcl
resource "azurerm_recovery_services_vault" "vault" {
  name                = "ContosoRecoveryVault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
}
```
- **azurerm_recovery_services_vault "vault"**: Creates a Recovery Services Vault for storing recovery points and backup data.

```hcl
resource "azurerm_site_recovery_replication_policy" "policy" {
  name                 = "ContosoReplicationPolicy"
  resource_group_name  = azurerm_resource_group.rg.name
  recovery_vault_name  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes = 1440
  application_consistent_snapshot_frequency_in_minutes = 60
}
```
- **azurerm_site_recovery_replication_policy "policy"**: Defines the replication policy for ASR with a 24-hour retention period and hourly application-consistent snapshots.

```hcl
resource "azurerm_sql_server" "sql" {
  name                         = "contososqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "ContosoEHRDB"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql.name
  sku_name            = "S1"
}
```
- **azurerm_sql_server "sql"**: Creates a SQL Server instance with administrative credentials.
- **azurerm_sql_database "sql_db"**: Creates a database named "ContosoEHRDB" on the SQL Server with a "S1" pricing tier.

```hcl
resource "azurerm_sql_failover_group" "failover_group" {
  name                = "ContosoFailoverGroup"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.sql.name
  databases           = [azurerm_sql_database.sql_db.id]

  partner_servers {
    id = azurerm_sql_server.sql.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 5
  }
}
```
- **azurerm_sql_failover_group "failover_group"**: Creates a failover group to enable automatic failover for the SQL database to a secondary server.

### 2. **Financial Services: Fabrikam Bank**

**Scenario: Azure Traffic Manager and SQL Database Geo-Replication**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "FabrikamBankRG"
  location = "East US"
}
```
- **provider "azurerm"**: Specifies the Azure provider for Terraform.
- **azurerm_resource_group "rg"**: Creates a resource group in the "East US" region named "FabrikamBankRG".

```hcl
resource "azurerm_traffic_manager_profile" "tm" {
  name                = "FabrikamTrafficManager"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  traffic_routing_method = "Priority"

  dns_config {
    relative_name = "fabrikam"
    ttl           = 30
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"
  }

  endpoint {
    name                = "Primary"
    target_resource_id  = azurerm_app_service.appservice.id
    endpoint_location   = azurerm_resource_group.rg.location
    priority            = 1
  }

  endpoint {
    name                = "Secondary"
    target_resource_id  = azurerm_app_service.appservice_secondary.id
    endpoint_location   = azurerm_resource_group.rg_secondary.location
    priority            = 2
  }
}
```
- **azurerm_traffic_manager_profile "tm"**: Configures a Traffic Manager profile to distribute traffic with a priority routing method.
  - **dns_config**: Configures DNS settings for the Traffic Manager.
  - **monitor_config**: Sets up health monitoring for endpoints.
  - **endpoint**: Defines the primary and secondary endpoints with priority settings.

```hcl
resource "azurerm_sql_server" "sql_primary" {
  name                         = "fabrikamprimarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_server" "sql_secondary" {
  name                         = "fabrikamsecondarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = "West US"
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "FabrikamDB"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql_primary.name
  sku_name            = "S1"
}
```
- **azurerm_sql_server "sql_primary"**: Creates the primary SQL Server in the "East US" region.
- **azurerm_sql_server "sql_secondary"**: Creates the secondary SQL Server in the "West US" region.
- **azurerm_sql_database "sql_db"**: Creates a database named "FabrikamDB" on the primary SQL Server.

```hcl
resource "azurerm_sql_failover_group" "failover_group" {
  name                = "FabrikamFailoverGroup"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.sql_primary.name
  databases           = [azurerm_sql_database.sql_db.id]

  partner_servers {
    id = azurerm_sql_server.sql_secondary.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 5
  }
}
```
- **azurerm_sql_failover_group "failover_group"**: Configures a failover group for automatic failover between the primary and secondary SQL Servers.

### 3. **Retail: Northwind Traders**

**Scenario: Azure Traffic Manager, Cosmos DB Global Distribution, and Azure Backup**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "NorthwindTradersRG"
  location = "Central US"
}
```
- **provider "azurerm"**: Specifies the Azure provider for Terraform.
- **azurerm_resource_group "rg"**: Creates a resource group in the "Central US" region named "NorthwindTradersRG".

```hcl
resource "azurerm_cosmosdb_account" "cosmosdb" {
  name                = "northwindcosmosdb"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = "East US"
    failover_priority = 0
  }

  geo_location {
    location          = "West US"
    failover_priority = 1
  }
}
```
- **azurerm_cosmosdb_account "cosmosdb"**: Configures a Cosmos DB account with global distribution.
  - **consistency_policy**: Sets the consistency level to "Session".
  - **geo_location**: Specifies the primary and secondary regions for replication.

```hcl
resource "azurerm_traffic_manager_profile" "tm" {
  name                = "NorthwindTrafficManager"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  traffic_routing_method = "Priority"

  dns_config {
    relative_name = "northwind"
    ttl           = 30
  }

  monitor_config {
    protocol = "HTTP"
    port     = 80
    path     = "/"


  }

  endpoint {
    name                = "Primary"
    target_resource_id  = azurerm_app_service.appservice.id
    endpoint_location   = azurerm_resource_group.rg.location
    priority            = 1
  }

  endpoint {
    name                = "Secondary"
    target_resource_id  = azurerm_app_service.appservice_secondary.id
    endpoint_location   = azurerm_resource_group.rg_secondary.location
    priority            = 2
  }
}
```
- **azurerm_traffic_manager_profile "tm"**: Sets up a Traffic Manager profile to route traffic with a priority routing method.
  - **dns_config**: Configures DNS settings.
  - **monitor_config**: Sets up health monitoring.
  - **endpoint**: Defines the primary and secondary endpoints with priorities.

```hcl
resource "azurerm_backup_policy_vm" "backup_policy" {
  name                = "NorthwindBackupPolicy"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_backup_vault.vault.name

  backup {
    frequency = "Daily"
    time      = "02:00"
  }

  retention_daily {
    count = 7
  }
}

resource "azurerm_backup_protected_vm" "protected_vm" {
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_backup_vault.vault.name
  source_vm_id        = azurerm_windows_virtual_machine.vm.id
  backup_policy_id    = azurerm_backup_policy_vm.backup_policy.id
}
```
- **azurerm_backup_policy_vm "backup_policy"**: Defines a daily backup policy for VMs with a 7-day retention period.
- **azurerm_backup_protected_vm "protected_vm"**: Protects a specific VM using the defined backup policy.

### 4. **Manufacturing: Contoso Manufacturing**

**Scenario: Azure IoT Hub, Azure Site Recovery, and Azure Monitor**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "ContosoManufacturingRG"
  location = "West Europe"
}
```
- **provider "azurerm"**: Specifies the Azure provider for Terraform.
- **azurerm_resource_group "rg"**: Creates a resource group in the "West Europe" region named "ContosoManufacturingRG".

```hcl
resource "azurerm_iothub" "iothub" {
  name                = "ContosoIoTHub"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku {
    name     = "S1"
    capacity = 1
  }
  retention_days = 7
}
```
- **azurerm_iothub "iothub"**: Sets up an IoT Hub with a "S1" SKU and 7-day data retention.

```hcl
resource "azurerm_recovery_services_vault" "vault" {
  name                = "ContosoRecoveryVault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                 = "ContosoReplicationPolicy"
  resource_group_name  = azurerm_resource_group.rg.name
  recovery_vault_name  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes = 1440
  application_consistent_snapshot_frequency_in_minutes = 60
}
```
- **azurerm_recovery_services_vault "vault"**: Creates a Recovery Services Vault for ASR.
- **azurerm_site_recovery_replication_policy "policy"**: Defines the replication policy for ASR with 24-hour retention and hourly application-consistent snapshots.

```hcl
resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "ContosoLogAnalytics"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
}

resource "azurerm_monitor_diagnostic_setting" "iot_diagnostics" {
  name               = "IoTHubDiagnostics"
  target_resource_id = azurerm_iothub.iothub.id

  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id

  log {
    category = "Connections"
    enabled  = true
  }

  log {
    category = "DeviceTelemetry"
    enabled  = true
  }

  log {
    category = "Routes"
    enabled  = true
  }

  log {
    category = "TwinUpdates"
    enabled  = true
  }
}
```
- **azurerm_log_analytics_workspace "log_analytics"**: Creates a Log Analytics workspace for monitoring.
- **azurerm_monitor_diagnostic_setting "iot_diagnostics"**: Configures diagnostics for the IoT Hub, sending logs to the Log Analytics workspace.

### 5. **Public Sector: City Government**

**Scenario: Azure Government Cloud, Azure Site Recovery, and SQL Database Geo-Replication**

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "CityGovRG"
  location = "US Gov Virginia"
}
```
- **provider "azurerm"**: Specifies the Azure provider for Terraform.
- **azurerm_resource_group "rg"**: Creates a resource group in the "US Gov Virginia" region named "CityGovRG".

```hcl
resource "azurerm_recovery_services_vault" "vault" {
  name                = "CityGovRecoveryVault"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                 = "CityGovReplicationPolicy"
  resource_group_name  = azurerm_resource_group.rg.name
  recovery_vault_name  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes = 1440
  application_consistent_snapshot_frequency_in_minutes = 60
}
```
- **azurerm_recovery_services_vault "vault"**: Creates a Recovery Services Vault for ASR.
- **azurerm_site_recovery_replication_policy "policy"**: Defines the replication policy for ASR with 24-hour retention and hourly application-consistent snapshots.

```hcl
resource "azurerm_sql_server" "sql_primary" {
  name                         = "citygovprimarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_server" "sql_secondary" {
  name                         = "citygovsecondarysql"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = "US Gov Texas"
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "CityGovDB"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql_primary.name
  sku_name            = "S1"
}
```
- **azurerm_sql_server "sql_primary"**: Creates the primary SQL Server in the "US Gov Virginia" region.
- **azurerm_sql_server "sql_secondary"**: Creates the secondary SQL Server in the "US Gov Texas" region.
- **azurerm_sql_database "sql_db"**: Creates a database named "CityGovDB" on the primary SQL Server.

```hcl
resource "azurerm_sql_failover_group" "failover_group" {
  name                = "CityGovFailoverGroup"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_sql_server.sql_primary.name
  databases           = [azurerm_sql_database.sql_db.id]

  partner_servers {
    id = azurerm_sql_server.sql_secondary.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 5
  }
}
```
- **azurerm_sql_failover_group "failover_group"**: Configures a failover group for automatic failover between the primary and secondary SQL Servers.

These Terraform scripts provide a foundational setup for disaster recovery in Azure. Depending on the organization's specific needs, additional configurations and resources might be required, such as networking, security, and compliance settings.
