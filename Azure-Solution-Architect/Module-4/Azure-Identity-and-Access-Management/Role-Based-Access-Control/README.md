Role-Based Access Control (RBAC) in Azure is a system that provides fine-grained access management for Azure resources. It allows you to assign roles to users, groups, service principals, and managed identities. By assigning roles, you can grant only the amount of access that users need to perform their jobs.

### Key Concepts of Azure RBAC

1. **Security Principal**: A security principal is an object that represents a user, group, service principal, or managed identity that is requesting access to Azure resources.

   - **User**: An individual who has a profile in Azure Active Directory.
   - **Group**: A set of users created in Azure Active Directory.
   - **Service Principal**: A security identity used by applications or services to access specific Azure resources.
   - **Managed Identity**: An identity in Azure AD that is automatically managed by Azure and used to authenticate to services.

2. **Role Definition**: A role definition is a collection of permissions. It's sometimes referred to as a role. A role definition lists the operations that can be performed, such as read, write, and delete. Azure has several built-in roles that you can use. Some common built-in roles are:

   - **Owner**: Full access to all resources, including the right to delegate access to others.
   - **Contributor**: Can create and manage all types of Azure resources but cannot grant access to others.
   - **Reader**: Can view existing Azure resources.
   - **User Access Administrator**: Can manage user access to Azure resources.

3. **Scope**: The scope is the set of resources that the access applies to. Azure has four levels of scope:

   - **Management Group**: A container for managing access, policies, and compliance across multiple subscriptions.
   - **Subscription**: A billing container for managing resources in Azure.
   - **Resource Group**: A container that holds related resources for an Azure solution.
   - **Resource**: A specific instance of a service, such as a virtual machine, storage account, or database.

4. **Role Assignment**: A role assignment is the process of attaching a role definition to a security principal at a particular scope for the purpose of granting access.

### How RBAC Works

When a user attempts to access an Azure resource, the system performs the following checks:

1. **Authentication**: Verifies the identity of the user, group, service principal, or managed identity through Azure Active Directory.
2. **Authorization**: Determines if the authenticated entity has the necessary permissions to perform the action. This involves checking the role assignments for the security principal at the requested scope.
3. **Permission Evaluation**: Evaluates whether the permissions defined in the role assignment allow the requested operation on the resource.

### Steps to Implement RBAC in Azure

1. **Identify Security Principals**: Determine who needs access to Azure resources (e.g., users, groups, service principals).
2. **Define Roles**: Decide which roles are needed and whether to use built-in roles or create custom roles.
3. **Assign Roles**: Assign the appropriate roles to the security principals at the correct scope.

### Managing RBAC in Azure

You can manage RBAC through various interfaces:

- **Azure Portal**: Provides a graphical interface to assign roles and manage access.
- **Azure CLI**: Allows for scripting and automation of role assignments using commands.
- **Azure PowerShell**: Another scripting option for managing RBAC.
- **Azure Resource Manager (ARM) Templates**: Define role assignments as part of your infrastructure as code deployments.
- **REST API**: Direct programmatic access to manage role assignments and definitions.

### Best Practices for Using RBAC

- **Least Privilege Principle**: Grant only the permissions necessary for users to perform their tasks.
- **Use Built-in Roles**: Prefer built-in roles where possible as they cover most scenarios and are maintained by Microsoft.
- **Audit Role Assignments**: Regularly review role assignments to ensure they are still appropriate.
- **Custom Roles**: Create custom roles when built-in roles do not meet your specific needs.

### Custom Roles

If the built-in roles do not meet your specific needs, you can create custom roles. A custom role consists of:

- **Actions**: Specifies the operations that are allowed.
- **NotActions**: Specifies the operations that are denied.
- **DataActions**: Specifies the data operations that are allowed.
- **NotDataActions**: Specifies the data operations that are denied.

Creating a custom role involves defining a JSON template that outlines the permissions and then using the Azure CLI, PowerShell, or REST API to create the role.

### Example of Creating a Custom Role

Here is an example of a JSON template for a custom role that allows read access to storage accounts and the ability to list keys:

```json
{
    "Name": "Custom Storage Reader",
    "Description": "Can read storage accounts and list keys",
    "Actions": [
        "Microsoft.Storage/storageAccounts/read",
        "Microsoft.Storage/storageAccounts/listkeys/action"
    ],
    "NotActions": [],
    "AssignableScopes": [
        "/subscriptions/{subscription-id}"
    ]
}
```

You can create this custom role using Azure CLI:

```sh
az role definition create --role-definition customRoleDefinition.json
```

RBAC in Azure provides a robust and flexible way to manage access to your resources, ensuring that users have the permissions they need while maintaining security and compliance.


Sure, here are detailed real-world examples of how Role-Based Access Control (RBAC) can be used in Azure across different industries:

### Example 1: Healthcare Industry

#### Scenario:
A healthcare provider needs to ensure that only authorized personnel can access sensitive patient data stored in an Azure SQL Database, while other staff members need access to various parts of the system for different purposes.

#### Implementation:
1. **Roles and Assignments**:
   - **Database Administrator (DBA)**: Full access to manage the Azure SQL Database.
   - **Medical Staff**: Read-only access to patient records.
   - **IT Support**: Access to manage the virtual machines and network components but no access to patient data.

2. **Role Definitions**:
   - **DBA**:
     - **Actions**: `Microsoft.Sql/servers/databases/*`
     - **Scope**: Subscription level
   - **Medical Staff**:
     - **Actions**: `Microsoft.Sql/servers/databases/read`
     - **Scope**: Specific database level
   - **IT Support**:
     - **Actions**: `Microsoft.Compute/*`, `Microsoft.Network/*`
     - **Scope**: Resource group level for infrastructure resources

3. **Implementation**:
   - Assign the DBA role to the database administrators at the subscription level.
   - Assign the Medical Staff role to doctors and nurses at the specific database level.
   - Assign the IT Support role to the IT team at the resource group level for virtual machines and network components.

#### Benefits:
- Ensures that only DBAs can modify the database schema.
- Medical staff can view patient data without the risk of accidental modification.
- IT support can maintain the infrastructure without accessing sensitive patient data.

### Example 2: Financial Services

#### Scenario:
A financial services company needs to control access to different parts of their trading platform hosted on Azure. They want to ensure that traders have access to trading tools, analysts have access to financial data, and administrators can manage the entire environment.

#### Implementation:
1. **Roles and Assignments**:
   - **Trading Platform Admin**: Full access to manage all resources related to the trading platform.
   - **Trader**: Access to trading applications and tools.
   - **Financial Analyst**: Access to financial data for analysis.

2. **Role Definitions**:
   - **Trading Platform Admin**:
     - **Actions**: `*`
     - **Scope**: Subscription level
   - **Trader**:
     - **Actions**: `Microsoft.Web/sites/*`, `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/*`
     - **Scope**: Resource group level for trading tools and applications
   - **Financial Analyst**:
     - **Actions**: `Microsoft.Sql/servers/databases/read`, `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`
     - **Scope**: Specific resource group containing financial data

3. **Implementation**:
   - Assign the Trading Platform Admin role to the platform administrators at the subscription level.
   - Assign the Trader role to the traders at the resource group level that contains trading tools.
   - Assign the Financial Analyst role to analysts at the resource group level that contains financial data.

#### Benefits:
- Administrators can manage all aspects of the trading platform.
- Traders have access to the tools they need without exposure to underlying infrastructure or sensitive data.
- Analysts can perform their analysis on financial data without affecting trading operations.

### Example 3: Manufacturing Industry

#### Scenario:
A manufacturing company uses Azure IoT to monitor and manage their production lines. They need to ensure that engineers have access to IoT devices and data, while managers have access to dashboards and reports.

#### Implementation:
1. **Roles and Assignments**:
   - **IoT Engineer**: Full access to manage IoT devices and data.
   - **Production Manager**: Access to view dashboards and reports.

2. **Role Definitions**:
   - **IoT Engineer**:
     - **Actions**: `Microsoft.Devices/IotHubs/*`, `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/*`
     - **Scope**: Resource group level for IoT resources
   - **Production Manager**:
     - **Actions**: `Microsoft.PowerBI/*/read`, `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`
     - **Scope**: Specific resource group containing dashboards and reports

3. **Implementation**:
   - Assign the IoT Engineer role to the engineers at the resource group level that contains IoT resources.
   - Assign the Production Manager role to managers at the resource group level that contains dashboards and reports.

#### Benefits:
- Engineers can fully manage IoT devices and access production data for troubleshooting and optimization.
- Managers can view operational dashboards and reports without interacting with the underlying data or devices.

### Example 4: Education Sector

#### Scenario:
A university uses Azure to host its student information system (SIS) and learning management system (LMS). Different access levels are required for administrators, faculty, and students.

#### Implementation:
1. **Roles and Assignments**:
   - **System Administrator**: Full access to manage all resources related to SIS and LMS.
   - **Faculty**: Access to course materials and student records.
   - **Student**: Access to personal records and course materials.

2. **Role Definitions**:
   - **System Administrator**:
     - **Actions**: `*`
     - **Scope**: Subscription level
   - **Faculty**:
     - **Actions**: `Microsoft.Web/sites/*`, `Microsoft.Sql/servers/databases/read`
     - **Scope**: Resource group level for LMS and SIS resources
   - **Student**:
     - **Actions**: `Microsoft.Web/sites/read`, `Microsoft.Sql/servers/databases/read`
     - **Scope**: Specific database containing student records

3. **Implementation**:
   - Assign the System Administrator role to IT admins at the subscription level.
   - Assign the Faculty role to professors and lecturers at the resource group level that contains LMS and SIS resources.
   - Assign the Student role to students at the specific database level that contains student records.

#### Benefits:
- System administrators can manage the entire infrastructure and applications.
- Faculty members can access and manage course materials and student records without altering system configurations.
- Students can access their personal data and course materials without affecting other users.

These examples illustrate how RBAC in Azure can be tailored to meet the specific needs of different industries and organizational structures, ensuring secure and efficient access to resources.


Certainly! Here are Terraform scripts for each of the real-world examples provided:

### Example 1: Healthcare Industry

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "healthcare-rg"
  location = "East US"
}

resource "azurerm_sql_server" "example" {
  name                         = "sqlserverexample"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "example" {
  name                = "sqldatabaseexample"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  server_name         = azurerm_sql_server.example.name
  edition             = "Basic"
}

resource "azurerm_role_assignment" "dba" {
  scope                = azurerm_sql_server.example.id
  role_definition_name = "Contributor"
  principal_id         = var.dba_principal_id
}

resource "azurerm_role_assignment" "medical_staff" {
  scope                = azurerm_sql_database.example.id
  role_definition_name = "Reader"
  principal_id         = var.medical_staff_principal_id
}

resource "azurerm_role_assignment" "it_support" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Contributor"
  principal_id         = var.it_support_principal_id
}
```

### Example 2: Financial Services

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "financial-rg"
  location = "West US"
}

resource "azurerm_app_service_plan" "example" {
  name                = "example-appserviceplan"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_app_service" "example" {
  name                = "example-appservice"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id
}

resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_role_assignment" "admin" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Owner"
  principal_id         = var.admin_principal_id
}

resource "azurerm_role_assignment" "trader" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Contributor"
  principal_id         = var.trader_principal_id
}

resource "azurerm_role_assignment" "analyst" {
  scope                = azurerm_storage_account.example.id
  role_definition_name = "Reader"
  principal_id         = var.analyst_principal_id
}
```

### Example 3: Manufacturing Industry

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "manufacturing-rg"
  location = "Central US"
}

resource "azurerm_iothub" "example" {
  name                = "example-iothub"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  sku {
    name     = "S1"
    capacity = 1
  }
}

resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_role_assignment" "iot_engineer" {
  scope                = azurerm_iothub.example.id
  role_definition_name = "Owner"
  principal_id         = var.iot_engineer_principal_id
}

resource "azurerm_role_assignment" "production_manager" {
  scope                = azurerm_storage_account.example.id
  role_definition_name = "Reader"
  principal_id         = var.production_manager_principal_id
}
```

### Example 4: Education Sector

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "education-rg"
  location = "East US 2"
}

resource "azurerm_sql_server" "example" {
  name                         = "sqlserverexample"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "example" {
  name                = "sqldatabaseexample"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  server_name         = azurerm_sql_server.example.name
  edition             = "Basic"
}

resource "azurerm_app_service_plan" "example" {
  name                = "example-appserviceplan"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_app_service" "example" {
  name                = "example-appservice"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id
}

resource "azurerm_role_assignment" "sys_admin" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Owner"
  principal_id         = var.sys_admin_principal_id
}

resource "azurerm_role_assignment" "faculty" {
  scope                = azurerm_sql_database.example.id
  role_definition_name = "Reader"
  principal_id         = var.faculty_principal_id
}

resource "azurerm_role_assignment" "student" {
  scope                = azurerm_sql_database.example.id
  role_definition_name = "Reader"
  principal_id         = var.student_principal_id
}
```

### Variables Definition Example

For each of these Terraform scripts, you will need to define the variables for the principal IDs (e.g., `dba_principal_id`, `trader_principal_id`, etc.). Here's an example of how you can define these variables in a `variables.tf` file:

```hcl
variable "dba_principal_id" {
  description = "Principal ID for the DBA role"
  type        = string
}

variable "medical_staff_principal_id" {
  description = "Principal ID for the Medical Staff role"
  type        = string
}

variable "it_support_principal_id" {
  description = "Principal ID for the IT Support role"
  type        = string
}

variable "admin_principal_id" {
  description = "Principal ID for the Admin role"
  type        = string
}

variable "trader_principal_id" {
  description = "Principal ID for the Trader role"
  type        = string
}

variable "analyst_principal_id" {
  description = "Principal ID for the Analyst role"
  type        = string
}

variable "iot_engineer_principal_id" {
  description = "Principal ID for the IoT Engineer role"
  type        = string
}

variable "production_manager_principal_id" {
  description = "Principal ID for the Production Manager role"
  type        = string
}

variable "sys_admin_principal_id" {
  description = "Principal ID for the System Administrator role"
  type        = string
}

variable "faculty_principal_id" {
  description = "Principal ID for the Faculty role"
  type        = string
}

variable "student_principal_id" {
  description = "Principal ID for the Student role"
  type        = string
}
```

This setup ensures that the necessary roles are assigned to the appropriate security principals, aligning with the specific needs of each industry scenario.


Certainly! Here are detailed explanations for each of the Terraform scripts provided:

### Example 1: Healthcare Industry

#### Explanation:
In this example, we are managing access to an Azure SQL Database for different roles within a healthcare provider.

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider block**: Configures the Azure provider to interact with Azure resources.

```hcl
resource "azurerm_resource_group" "example" {
  name     = "healthcare-rg"
  location = "East US"
}
```
- **Resource Group**: A container that holds related resources for the healthcare solution.

```hcl
resource "azurerm_sql_server" "example" {
  name                         = "sqlserverexample"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}
```
- **SQL Server**: Sets up an Azure SQL Server to host the database.

```hcl
resource "azurerm_sql_database" "example" {
  name                = "sqldatabaseexample"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  server_name         = azurerm_sql_server.example.name
  edition             = "Basic"
}
```
- **SQL Database**: Creates a SQL Database within the SQL Server.

```hcl
resource "azurerm_role_assignment" "dba" {
  scope                = azurerm_sql_server.example.id
  role_definition_name = "Contributor"
  principal_id         = var.dba_principal_id
}
```
- **Role Assignment for DBA**: Assigns the Contributor role to the DBA principal at the SQL Server scope, allowing full management of the server.

```hcl
resource "azurerm_role_assignment" "medical_staff" {
  scope                = azurerm_sql_database.example.id
  role_definition_name = "Reader"
  principal_id         = var.medical_staff_principal_id
}
```
- **Role Assignment for Medical Staff**: Assigns the Reader role to the Medical Staff principal at the SQL Database scope, allowing read-only access to patient data.

```hcl
resource "azurerm_role_assignment" "it_support" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Contributor"
  principal_id         = var.it_support_principal_id
}
```
- **Role Assignment for IT Support**: Assigns the Contributor role to the IT Support principal at the Resource Group scope, allowing management of infrastructure resources within the resource group.

### Example 2: Financial Services

#### Explanation:
In this example, we are controlling access to resources related to a trading platform for different roles within a financial services company.

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider block**: Configures the Azure provider to interact with Azure resources.

```hcl
resource "azurerm_resource_group" "example" {
  name     = "financial-rg"
  location = "West US"
}
```
- **Resource Group**: A container that holds related resources for the financial solution.

```hcl
resource "azurerm_app_service_plan" "example" {
  name                = "example-appserviceplan"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}
```
- **App Service Plan**: Configures the App Service Plan for hosting web applications.

```hcl
resource "azurerm_app_service" "example" {
  name                = "example-appservice"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id
}
```
- **App Service**: Creates an App Service for hosting a web application.

```hcl
resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **Storage Account**: Sets up a storage account for storing data.

```hcl
resource "azurerm_role_assignment" "admin" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Owner"
  principal_id         = var.admin_principal_id
}
```
- **Role Assignment for Admin**: Assigns the Owner role to the Admin principal at the Resource Group scope, allowing full management of all resources within the resource group.

```hcl
resource "azurerm_role_assignment" "trader" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Contributor"
  principal_id         = var.trader_principal_id
}
```
- **Role Assignment for Trader**: Assigns the Contributor role to the Trader principal at the Resource Group scope, allowing access to trading applications and tools.

```hcl
resource "azurerm_role_assignment" "analyst" {
  scope                = azurerm_storage_account.example.id
  role_definition_name = "Reader"
  principal_id         = var.analyst_principal_id
}
```
- **Role Assignment for Analyst**: Assigns the Reader role to the Analyst principal at the Storage Account scope, allowing read-only access to financial data.

### Example 3: Manufacturing Industry

#### Explanation:
In this example, we are managing access to IoT resources and production data for different roles within a manufacturing company.

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider block**: Configures the Azure provider to interact with Azure resources.

```hcl
resource "azurerm_resource_group" "example" {
  name     = "manufacturing-rg"
  location = "Central US"
}
```
- **Resource Group**: A container that holds related resources for the manufacturing solution.

```hcl
resource "azurerm_iothub" "example" {
  name                = "example-iothub"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  sku {
    name     = "S1"
    capacity = 1
  }
}
```
- **IoT Hub**: Sets up an IoT Hub to manage IoT devices.

```hcl
resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **Storage Account**: Configures a storage account for storing IoT data.

```hcl
resource "azurerm_role_assignment" "iot_engineer" {
  scope                = azurerm_iothub.example.id
  role_definition_name = "Owner"
  principal_id         = var.iot_engineer_principal_id
}
```
- **Role Assignment for IoT Engineer**: Assigns the Owner role to the IoT Engineer principal at the IoT Hub scope, allowing full management of IoT devices and data.

```hcl
resource "azurerm_role_assignment" "production_manager" {
  scope                = azurerm_storage_account.example.id
  role_definition_name = "Reader"
  principal_id         = var.production_manager_principal_id
}
```
- **Role Assignment for Production Manager**: Assigns the Reader role to the Production Manager principal at the Storage Account scope, allowing read-only access to production data.

### Example 4: Education Sector

#### Explanation:
In this example, we are managing access to resources related to a student information system (SIS) and learning management system (LMS) for different roles within a university.

```hcl
provider "azurerm" {
  features {}
}
```
- **Provider block**: Configures the Azure provider to interact with Azure resources.

```hcl
resource "azurerm_resource_group" "example" {
  name     = "education-rg"
  location = "East US 2"
}
```
- **Resource Group**: A container that holds related resources for the education solution.

```hcl
resource "azurerm_sql_server" "example" {
  name                         = "sqlserverexample"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}
```
- **SQL Server**: Sets up an Azure SQL Server to host the database for the SIS and LMS.

```hcl
resource "azurerm_sql_database" "example" {
  name                = "sqldatabaseexample"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  server_name         = azurerm_sql_server.example.name
  edition             = "Basic"
}
```
- **SQL Database**: Creates a SQL Database within the SQL Server.

```hcl
resource "azurerm_app_service_plan"

 "example" {
  name                = "example-appserviceplan"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}
```
- **App Service Plan**: Configures the App Service Plan for hosting web applications.

```hcl
resource "azurerm_app_service" "example" {
  name                = "example-appservice"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id
}
```
- **App Service**: Creates an App Service for hosting the LMS and SIS web applications.

```hcl
resource "azurerm_role_assignment" "sys_admin" {
  scope                = azurerm_resource_group.example.id
  role_definition_name = "Owner"
  principal_id         = var.sys_admin_principal_id
}
```
- **Role Assignment for System Administrator**: Assigns the Owner role to the System Administrator principal at the Resource Group scope, allowing full management of all resources within the resource group.

```hcl
resource "azurerm_role_assignment" "faculty" {
  scope                = azurerm_sql_database.example.id
  role_definition_name = "Reader"
  principal_id         = var.faculty_principal_id
}
```
- **Role Assignment for Faculty**: Assigns the Reader role to the Faculty principal at the SQL Database scope, allowing read-only access to student records and course materials.

```hcl
resource "azurerm_role_assignment" "student" {
  scope                = azurerm_sql_database.example.id
  role_definition_name = "Reader"
  principal_id         = var.student_principal_id
}
```
- **Role Assignment for Student**: Assigns the Reader role to the Student principal at the SQL Database scope, allowing read-only access to personal records and course materials.

### Variables Definition Example

To manage the principal IDs, you will need to define variables in a separate `variables.tf` file, as shown in the previous response.

### Summary

Each of these Terraform scripts is designed to configure the necessary Azure resources and assign RBAC roles to appropriate security principals based on the specific requirements of different industries. These scripts help ensure that access to resources is managed securely and efficiently, aligning with the principles of least privilege and role-based access control.
