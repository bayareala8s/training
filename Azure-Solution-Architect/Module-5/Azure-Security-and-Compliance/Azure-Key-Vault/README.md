Azure Key Vault is a cloud service provided by Microsoft Azure for securely storing and accessing secrets, such as API keys, passwords, certificates, and cryptographic keys. It is designed to help safeguard cryptographic keys and secrets used by cloud applications and services. Here is a detailed explanation of its key features, use cases, and how it works:

### Key Features

1. **Secret Management**: Securely store and manage sensitive data such as passwords, connection strings, and API keys. Secrets can be stored and retrieved programmatically.

2. **Key Management**: Manage cryptographic keys used for data encryption. Key Vault supports both software-protected and Hardware Security Module (HSM)-protected keys.

3. **Certificate Management**: Simplifies the process of creating and managing SSL/TLS certificates. Key Vault can enroll certificates from supported public Certificate Authorities (CAs) and can also manage the lifecycle of these certificates, including renewal and rotation.

4. **Access Policies**: Provides fine-grained access control via Azure Active Directory (AAD). You can define who or what can access the secrets and keys.

5. **Audit Logging**: Every access to the Key Vault is logged and can be integrated with Azure Monitor logs to monitor and alert on critical events.

6. **Integration with Azure Services**: Key Vault integrates seamlessly with other Azure services such as Azure Functions, Azure App Service, and Azure Virtual Machines, allowing these services to securely access secrets and keys.

### Use Cases

1. **Secure Storage of Secrets**: Store application secrets like database connection strings, API keys, and passwords securely.

2. **Data Encryption**: Use cryptographic keys stored in Key Vault to encrypt and decrypt data, ensuring that encryption keys are securely stored and managed.

3. **Certificate Management**: Simplify SSL/TLS certificate management for your web applications, ensuring certificates are always up-to-date and reducing the risk of expired certificates causing service disruptions.

4. **Secure DevOps Practices**: Integrate Key Vault with DevOps pipelines to securely manage secrets and keys during the development and deployment processes.

5. **Compliance and Security**: Use Key Vault to help meet regulatory and compliance requirements by ensuring that sensitive data is encrypted and access to keys and secrets is tightly controlled and auditable.

### How It Works

1. **Create a Key Vault**: Use the Azure portal, Azure CLI, or Azure PowerShell to create a new Key Vault in your Azure subscription. During creation, you specify the region and resource group.

2. **Add Secrets, Keys, and Certificates**: Once the Key Vault is created, you can add secrets, keys, and certificates. For example, you can add a secret through the Azure portal or by using the Azure CLI command `az keyvault secret set`.

3. **Set Access Policies**: Define who or what can access the Key Vault and its contents. Access policies can be set to grant or deny permissions to specific users, groups, or applications.

4. **Accessing Secrets and Keys**: Applications and services can programmatically access the contents of the Key Vault using Azure SDKs, REST APIs, or through integrations with other Azure services. For example, an application can retrieve a secret by making a call to the Key Vault's REST API with the appropriate credentials.

5. **Monitoring and Auditing**: All interactions with the Key Vault are logged. You can monitor these logs to ensure that access to sensitive data is tracked and to detect any unauthorized access attempts.

### Example Scenario

**Scenario: Storing and Accessing Database Connection Strings**

1. **Step 1: Create a Key Vault**
   ```bash
   az keyvault create --name MyKeyVault --resource-group MyResourceGroup --location eastus
   ```

2. **Step 2: Add a Secret**
   ```bash
   az keyvault secret set --vault-name MyKeyVault --name MyDbConnectionString --value "Server=myserver.database.windows.net;Database=mydb;User Id=myuser;Password=mypassword;"
   ```

3. **Step 3: Set Access Policies**
   ```bash
   az keyvault set-policy --name MyKeyVault --upn user@domain.com --secret-permissions get
   ```

4. **Step 4: Access the Secret in an Application**
   ```python
   from azure.identity import DefaultAzureCredential
   from azure.keyvault.secrets import SecretClient

   key_vault_name = "MyKeyVault"
   kv_uri = f"https://{key_vault_name}.vault.azure.net"

   credential = DefaultAzureCredential()
   client = SecretClient(vault_url=kv_uri, credential=credential)

   retrieved_secret = client.get_secret("MyDbConnectionString")
   connection_string = retrieved_secret.value

   print(f"Database Connection String: {connection_string}")
   ```

### Best Practices

1. **Least Privilege**: Grant the minimum permissions necessary to users and applications.
2. **Automated Key Rotation**: Implement automated rotation of secrets and keys to reduce the risk of exposure.
3. **Use Managed Identities**: Leverage managed identities for Azure resources to access Key Vault without needing to manage credentials.
4. **Regular Auditing**: Regularly audit access logs and policies to ensure compliance and security.

Azure Key Vault is a powerful tool for managing and securing access to sensitive information in your cloud applications. By following best practices and leveraging its features, you can enhance the security and compliance of your cloud infrastructure.


### Real-World Examples of Using Azure Key Vault

#### 1. **Financial Services: Secure Transaction Processing**
A global bank needs to ensure the security and integrity of its online transaction processing system. They handle millions of transactions daily, and it's crucial that sensitive information such as API keys, database connection strings, and cryptographic keys are securely managed.

**Implementation:**
- **Secrets Management**: The bank uses Azure Key Vault to store API keys and connection strings for their transaction processing application. This ensures that sensitive information is not hardcoded in application code or stored in configuration files.
- **Key Management**: Cryptographic keys used for encrypting transaction data are stored in Azure Key Vault. These keys are used to encrypt data at rest and in transit, ensuring that transaction data is secure.
- **Access Policies**: Only the transaction processing application and a select group of administrators have access to the keys and secrets in the Key Vault. This is enforced using Azure Active Directory (AAD) and access policies in Key Vault.
- **Audit Logging**: Every access to the Key Vault is logged and monitored using Azure Monitor logs, helping the bank to detect any unauthorized access attempts.

#### 2. **Healthcare: Securing Patient Data**
A healthcare provider needs to comply with regulatory requirements such as HIPAA, which mandates the protection of patient data. They are migrating their patient management system to Azure and need to ensure that sensitive data is protected.

**Implementation:**
- **Secrets Management**: Patient management applications store sensitive information such as database connection strings, API keys, and authentication tokens in Azure Key Vault. This ensures that only authorized applications can access this sensitive data.
- **Key Management**: The healthcare provider uses Azure Key Vault to store cryptographic keys used for encrypting patient records. These keys are HSM-protected to meet regulatory requirements.
- **Certificate Management**: SSL/TLS certificates used for securing communications between patient management applications and databases are stored and managed in Azure Key Vault. This ensures that certificates are always up-to-date and automatically renewed.
- **Access Policies**: Access to the Key Vault is tightly controlled using Azure Active Directory. Only authorized applications and personnel can access the keys, secrets, and certificates.
- **Monitoring and Auditing**: All access to the Key Vault is logged and integrated with Azure Monitor logs. This enables the healthcare provider to monitor access and detect any suspicious activities, ensuring compliance with regulatory requirements.

#### 3. **E-Commerce: Protecting Customer Data**
An e-commerce company needs to secure customer data and payment information. They want to ensure that their application is secure and that sensitive information is not exposed.

**Implementation:**
- **Secrets Management**: The e-commerce application stores sensitive information such as payment gateway API keys, database connection strings, and encryption keys in Azure Key Vault. This prevents exposure of sensitive information in the application code or configuration files.
- **Key Management**: Cryptographic keys used for encrypting customer data and payment information are stored in Azure Key Vault. This ensures that customer data is encrypted at rest and in transit.
- **Certificate Management**: SSL/TLS certificates used for securing communications between the e-commerce application and payment gateway are stored and managed in Azure Key Vault. This ensures secure communication and protects customer payment information.
- **Access Policies**: Access to the Key Vault is restricted to the e-commerce application and a few administrators using Azure Active Directory. Access policies are defined to grant the minimum necessary permissions.
- **Automated Key Rotation**: The e-commerce company has implemented automated rotation of keys and secrets stored in Azure Key Vault. This reduces the risk of exposure and ensures that keys and secrets are regularly updated.

#### 4. **DevOps: Secure CI/CD Pipelines**
A software development company uses continuous integration and continuous deployment (CI/CD) pipelines to deploy applications to Azure. They need to manage secrets and keys securely during the build and deployment processes.

**Implementation:**
- **Secrets Management**: CI/CD pipelines use Azure Key Vault to store sensitive information such as API keys, database connection strings, and authentication tokens. This ensures that secrets are not stored in source code repositories or CI/CD configuration files.
- **Key Management**: Keys used for signing code and encrypting artifacts are stored in Azure Key Vault. This ensures that keys are securely managed and only accessible to the CI/CD pipeline.
- **Access Policies**: Access to the Key Vault is restricted to the CI/CD pipeline and a few administrators using Azure Active Directory. Access policies are defined to grant the minimum necessary permissions.
- **Integration with CI/CD Tools**: The CI/CD pipeline is integrated with Azure Key Vault using service principals. This allows the pipeline to securely retrieve secrets and keys during the build and deployment processes.
- **Audit Logging**: All access to the Key Vault is logged and monitored using Azure Monitor logs. This helps the company to detect any unauthorized access attempts and ensure the security of their CI/CD pipelines.

#### 5. **Manufacturing: Secure IoT Solutions**
A manufacturing company uses IoT devices to monitor and control equipment on the factory floor. They need to ensure that the communication between IoT devices and the cloud is secure and that sensitive information such as device credentials and encryption keys are protected.

**Implementation:**
- **Secrets Management**: IoT devices store device credentials and API keys in Azure Key Vault. This ensures that sensitive information is not hardcoded in the device firmware or configuration files.
- **Key Management**: Cryptographic keys used for securing communication between IoT devices and the cloud are stored in Azure Key Vault. These keys are used to encrypt data transmitted between the devices and the cloud, ensuring secure communication.
- **Access Policies**: Access to the Key Vault is restricted to the IoT devices and a few administrators using Azure Active Directory. Access policies are defined to grant the minimum necessary permissions.
- **Certificate Management**: SSL/TLS certificates used for securing communication between IoT devices and the cloud are stored and managed in Azure Key Vault. This ensures that certificates are always up-to-date and automatically renewed.
- **Monitoring and Auditing**: All access to the Key Vault is logged and monitored using Azure Monitor logs. This helps the company to detect any unauthorized access attempts and ensure the security of their IoT solutions.

These examples demonstrate how Azure Key Vault can be used in various industries to secure sensitive information, manage cryptographic keys, and ensure compliance with regulatory requirements. By leveraging Azure Key Vault, organizations can enhance the security and integrity of their applications and data.


Here are Terraform scripts for each of the real-world examples provided. These scripts will help you create and configure Azure Key Vault and its related components for each scenario.

### Example 1: Financial Services - Secure Transaction Processing

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-financial-services"
  location = "East US"
}

resource "azurerm_key_vault" "example" {
  name                = "kv-financial-services"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id           = data.azurerm_client_config.example.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.example.tenant_id
    object_id = data.azurerm_client_config.example.object_id

    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover",
    ]

    key_permissions = [
      "get",
      "create",
      "delete",
      "list",
      "update",
      "recover",
    ]
  }
}

resource "azurerm_key_vault_secret" "example" {
  name         = "db-connection-string"
  value        = "Server=myserver.database.windows.net;Database=mydb;User Id=myuser;Password=mypassword;"
  key_vault_id = azurerm_key_vault.example.id
}

data "azurerm_client_config" "example" {}
```

### Example 2: Healthcare - Securing Patient Data

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-healthcare"
  location = "East US"
}

resource "azurerm_key_vault" "example" {
  name                = "kv-healthcare"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id           = data.azurerm_client_config.example.tenant_id
  sku_name            = "premium" # HSM-protected keys

  access_policy {
    tenant_id = data.azurerm_client_config.example.tenant_id
    object_id = data.azurerm_client_config.example.object_id

    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover",
    ]

    key_permissions = [
      "get",
      "create",
      "delete",
      "list",
      "update",
      "recover",
    ]

    certificate_permissions = [
      "get",
      "list",
      "update",
      "create",
      "import",
      "delete",
      "recover",
    ]
  }
}

resource "azurerm_key_vault_secret" "example" {
  name         = "db-connection-string"
  value        = "Server=myserver.database.windows.net;Database=mydb;User Id=myuser;Password=mypassword;"
  key_vault_id = azurerm_key_vault.example.id
}

data "azurerm_client_config" "example" {}
```

### Example 3: E-Commerce - Protecting Customer Data

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-ecommerce"
  location = "East US"
}

resource "azurerm_key_vault" "example" {
  name                = "kv-ecommerce"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id           = data.azurerm_client_config.example.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.example.tenant_id
    object_id = data.azurerm_client_config.example.object_id

    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover",
    ]

    key_permissions = [
      "get",
      "create",
      "delete",
      "list",
      "update",
      "recover",
    ]

    certificate_permissions = [
      "get",
      "list",
      "update",
      "create",
      "import",
      "delete",
      "recover",
    ]
  }
}

resource "azurerm_key_vault_secret" "example" {
  name         = "payment-gateway-api-key"
  value        = "your_payment_gateway_api_key"
  key_vault_id = azurerm_key_vault.example.id
}

data "azurerm_client_config" "example" {}
```

### Example 4: DevOps - Secure CI/CD Pipelines

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-devops"
  location = "East US"
}

resource "azurerm_key_vault" "example" {
  name                = "kv-devops"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id           = data.azurerm_client_config.example.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.example.tenant_id
    object_id = data.azurerm_client_config.example.object_id

    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover",
    ]

    key_permissions = [
      "get",
      "create",
      "delete",
      "list",
      "update",
      "recover",
    ]
  }
}

resource "azurerm_key_vault_secret" "example" {
  name         = "ci-cd-secret"
  value        = "your_ci_cd_secret_value"
  key_vault_id = azurerm_key_vault.example.id
}

data "azurerm_client_config" "example" {}
```

### Example 5: Manufacturing - Secure IoT Solutions

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-manufacturing"
  location = "East US"
}

resource "azurerm_key_vault" "example" {
  name                = "kv-manufacturing"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id           = data.azurerm_client_config.example.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.example.tenant_id
    object_id = data.azurerm_client_config.example.object_id

    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover",
    ]

    key_permissions = [
      "get",
      "create",
      "delete",
      "list",
      "update",
      "recover",
    ]

    certificate_permissions = [
      "get",
      "list",
      "update",
      "create",
      "import",
      "delete",
      "recover",
    ]
  }
}

resource "azurerm_key_vault_secret" "example" {
  name         = "iot-device-credential"
  value        = "your_iot_device_credential"
  key_vault_id = azurerm_key_vault.example.id
}

data "azurerm_client_config" "example" {}
```

These Terraform scripts create an Azure Key Vault, configure access policies, and add secrets for each specific use case. You can further customize these scripts based on your specific requirements and integrate them into your infrastructure as code (IaC) practices.



Sure! Here’s a step-by-step explanation for each of the Terraform scripts provided, tailored to each real-world example.

### Example 1: Financial Services - Secure Transaction Processing

#### Step-by-Step Explanation:

1. **Provider Configuration:**
    ```hcl
    provider "azurerm" {
      features {}
    }
    ```
    - This configures the Azure provider, which allows Terraform to interact with Azure resources.

2. **Resource Group Creation:**
    ```hcl
    resource "azurerm_resource_group" "example" {
      name     = "rg-financial-services"
      location = "East US"
    }
    ```
    - Creates a resource group named `rg-financial-services` in the East US region.

3. **Key Vault Creation:**
    ```hcl
    resource "azurerm_key_vault" "example" {
      name                = "kv-financial-services"
      location            = azurerm_resource_group.example.location
      resource_group_name = azurerm_resource_group.example.name
      tenant_id           = data.azurerm_client_config.example.tenant_id
      sku_name            = "standard"
    ```
    - Creates a Key Vault named `kv-financial-services` in the previously created resource group.
    - Uses the `standard` SKU.
    - The `tenant_id` is fetched dynamically using the `azurerm_client_config` data source.

4. **Access Policy Configuration:**
    ```hcl
    access_policy {
      tenant_id = data.azurerm_client_config.example.tenant_id
      object_id = data.azurerm_client_config.example.object_id

      secret_permissions = [
        "get",
        "list",
        "set",
        "delete",
        "recover",
      ]

      key_permissions = [
        "get",
        "create",
        "delete",
        "list",
        "update",
        "recover",
      ]
    }
    ```
    - Defines access policies for the Key Vault.
    - Grants the current user or service principal permissions for secrets and keys.

5. **Adding a Secret:**
    ```hcl
    resource "azurerm_key_vault_secret" "example" {
      name         = "db-connection-string"
      value        = "Server=myserver.database.windows.net;Database=mydb;User Id=myuser;Password=mypassword;"
      key_vault_id = azurerm_key_vault.example.id
    }
    ```
    - Adds a secret named `db-connection-string` with a value representing a database connection string.

6. **Client Configuration Data Source:**
    ```hcl
    data "azurerm_client_config" "example" {}
    ```
    - Retrieves information about the current Azure client configuration.

### Example 2: Healthcare - Securing Patient Data

#### Step-by-Step Explanation:

1. **Provider Configuration:**
    ```hcl
    provider "azurerm" {
      features {}
    }
    ```
    - Configures the Azure provider.

2. **Resource Group Creation:**
    ```hcl
    resource "azurerm_resource_group" "example" {
      name     = "rg-healthcare"
      location = "East US"
    }
    ```
    - Creates a resource group named `rg-healthcare`.

3. **Key Vault Creation:**
    ```hcl
    resource "azurerm_key_vault" "example" {
      name                = "kv-healthcare"
      location            = azurerm_resource_group.example.location
      resource_group_name = azurerm_resource_group.example.name
      tenant_id           = data.azurerm_client_config.example.tenant_id
      sku_name            = "premium"
    ```
    - Creates a Key Vault named `kv-healthcare` using the `premium` SKU for HSM-protected keys.

4. **Access Policy Configuration:**
    ```hcl
    access_policy {
      tenant_id = data.azurerm_client_config.example.tenant_id
      object_id = data.azurerm_client_config.example.object_id

      secret_permissions = [
        "get",
        "list",
        "set",
        "delete",
        "recover",
      ]

      key_permissions = [
        "get",
        "create",
        "delete",
        "list",
        "update",
        "recover",
      ]

      certificate_permissions = [
        "get",
        "list",
        "update",
        "create",
        "import",
        "delete",
        "recover",
      ]
    }
    ```
    - Grants access permissions for secrets, keys, and certificates.

5. **Adding a Secret:**
    ```hcl
    resource "azurerm_key_vault_secret" "example" {
      name         = "db-connection-string"
      value        = "Server=myserver.database.windows.net;Database=mydb;User Id=myuser;Password=mypassword;"
      key_vault_id = azurerm_key_vault.example.id
    }
    ```
    - Adds a secret named `db-connection-string`.

6. **Client Configuration Data Source:**
    ```hcl
    data "azurerm_client_config" "example" {}
    ```
    - Retrieves the Azure client configuration.

### Example 3: E-Commerce - Protecting Customer Data

#### Step-by-Step Explanation:

1. **Provider Configuration:**
    ```hcl
    provider "azurerm" {
      features {}
    }
    ```
    - Configures the Azure provider.

2. **Resource Group Creation:**
    ```hcl
    resource "azurerm_resource_group" "example" {
      name     = "rg-ecommerce"
      location = "East US"
    }
    ```
    - Creates a resource group named `rg-ecommerce`.

3. **Key Vault Creation:**
    ```hcl
    resource "azurerm_key_vault" "example" {
      name                = "kv-ecommerce"
      location            = azurerm_resource_group.example.location
      resource_group_name = azurerm_resource_group.example.name
      tenant_id           = data.azurerm_client_config.example.tenant_id
      sku_name            = "standard"
    ```
    - Creates a Key Vault named `kv-ecommerce`.

4. **Access Policy Configuration:**
    ```hcl
    access_policy {
      tenant_id = data.azurerm_client_config.example.tenant_id
      object_id = data.azurerm_client_config.example.object_id

      secret_permissions = [
        "get",
        "list",
        "set",
        "delete",
        "recover",
      ]

      key_permissions = [
        "get",
        "create",
        "delete",
        "list",
        "update",
        "recover",
      ]

      certificate_permissions = [
        "get",
        "list",
        "update",
        "create",
        "import",
        "delete",
        "recover",
      ]
    }
    ```
    - Defines access policies for secrets, keys, and certificates.

5. **Adding a Secret:**
    ```hcl
    resource "azurerm_key_vault_secret" "example" {
      name         = "payment-gateway-api-key"
      value        = "your_payment_gateway_api_key"
      key_vault_id = azurerm_key_vault.example.id
    }
    ```
    - Adds a secret named `payment-gateway-api-key`.

6. **Client Configuration Data Source:**
    ```hcl
    data "azurerm_client_config" "example" {}
    ```
    - Retrieves the Azure client configuration.

### Example 4: DevOps - Secure CI/CD Pipelines

#### Step-by-Step Explanation:

1. **Provider Configuration:**
    ```hcl
    provider "azurerm" {
      features {}
    }
    ```
    - Configures the Azure provider.

2. **Resource Group Creation:**
    ```hcl
    resource "azurerm_resource_group" "example" {
      name     = "rg-devops"
      location = "East US"
    }
    ```
    - Creates a resource group named `rg-devops`.

3. **Key Vault Creation:**
    ```hcl
    resource "azurerm_key_vault" "example" {
      name                = "kv-devops"
      location            = azurerm_resource_group.example.location
      resource_group_name = azurerm_resource_group.example.name
      tenant_id           = data.azurerm_client_config.example.tenant_id
      sku_name            = "standard"
    ```
    - Creates a Key Vault named `kv-devops`.

4. **Access Policy Configuration:**
    ```hcl
    access_policy {
      tenant_id = data.azurerm_client_config.example.tenant_id
      object_id = data.azurerm_client_config.example.object_id

      secret_permissions = [
        "get",
        "list",
        "set",
        "delete",
        "recover",
      ]

      key_permissions = [
        "get",
        "create",
        "delete",
        "list",
        "update",
        "recover",
      ]
    }
    ```
    - Defines access policies for secrets and keys.

5. **Adding a Secret:**
    ```hcl
    resource "azurerm_key_vault_secret" "example" {
      name         = "ci-cd-secret"
      value        = "your_ci_cd_secret_value"
      key_vault_id = azurerm_key_vault.example.id
    }
    ```
    - Adds a secret named `ci-cd-secret`.

6. **Client Configuration Data Source:**
    ```hcl
    data "azurerm_client_config" "example" {}
    ```
    - Retrieves the Azure client configuration.

### Example 5: Manufacturing - Secure IoT Solutions

#### Step-by-Step Explanation:

1. **Provider Configuration:**
    ```hcl
    provider "az

urerm" {
      features {}
    }
    ```
    - Configures the Azure provider.

2. **Resource Group Creation:**
    ```hcl
    resource "azurerm_resource_group" "example" {
      name     = "rg-manufacturing"
      location = "East US"
    }
    ```
    - Creates a resource group named `rg-manufacturing`.

3. **Key Vault Creation:**
    ```hcl
    resource "azurerm_key_vault" "example" {
      name                = "kv-manufacturing"
      location            = azurerm_resource_group.example.location
      resource_group_name = azurerm_resource_group.example.name
      tenant_id           = data.azurerm_client_config.example.tenant_id
      sku_name            = "standard"
    ```
    - Creates a Key Vault named `kv-manufacturing`.

4. **Access Policy Configuration:**
    ```hcl
    access_policy {
      tenant_id = data.azurerm_client_config.example.tenant_id
      object_id = data.azurerm_client_config.example.object_id

      secret_permissions = [
        "get",
        "list",
        "set",
        "delete",
        "recover",
      ]

      key_permissions = [
        "get",
        "create",
        "delete",
        "list",
        "update",
        "recover",
      ]

      certificate_permissions = [
        "get",
        "list",
        "update",
        "create",
        "import",
        "delete",
        "recover",
      ]
    }
    ```
    - Defines access policies for secrets, keys, and certificates.

5. **Adding a Secret:**
    ```hcl
    resource "azurerm_key_vault_secret" "example" {
      name         = "iot-device-credential"
      value        = "your_iot_device_credential"
      key_vault_id = azurerm_key_vault.example.id
    }
    ```
    - Adds a secret named `iot-device-credential`.

6. **Client Configuration Data Source:**
    ```hcl
    data "azurerm_client_config" "example" {}
    ```
    - Retrieves the Azure client configuration.

These step-by-step explanations cover the key components of each Terraform script, explaining how they work together to create and configure Azure Key Vault for various use cases.
