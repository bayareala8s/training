Azure Content Delivery Network (CDN) is a distributed network of servers designed to efficiently deliver web content to users around the world. By caching content on strategically placed edge servers, Azure CDN can reduce latency, increase performance, and improve user experience. Here's a detailed explanation of its components and how it works:

### Key Components of Azure CDN

1. **POP (Point of Presence) Locations**:
   - These are the strategically placed servers around the world where content is cached. When a user requests content, the nearest POP serves the content, reducing latency.

2. **Origin Server**:
   - This is the server where the original content is stored. It could be an Azure Storage account, a web app, or any other publicly accessible web server.

3. **CDN Endpoint**:
   - The endpoint is the URL through which the CDN serves the cached content. This endpoint is created when you set up a CDN profile in Azure.

### How Azure CDN Works

1. **Content Request**:
   - When a user requests a piece of content (e.g., an image or a video), the request is routed to the nearest POP.

2. **Cache Check**:
   - The POP checks if it has a cached copy of the requested content.
   - If the content is already cached (a cache hit), it is served directly from the POP.
   - If the content is not cached (a cache miss), the POP fetches the content from the origin server.

3. **Content Delivery**:
   - Once the content is fetched from the origin server, it is cached in the POP for future requests and simultaneously delivered to the user.

4. **Caching Rules**:
   - You can define caching rules to control how and when content is cached. This includes setting expiration times and customizing caching behavior based on HTTP headers.

### Benefits of Using Azure CDN

1. **Improved Performance**:
   - By caching content closer to users, Azure CDN reduces latency and load times, leading to faster content delivery.

2. **Scalability**:
   - Azure CDN can handle large amounts of traffic, providing a scalable solution for content delivery.

3. **Global Reach**:
   - With a network of POPs around the globe, Azure CDN ensures that content is delivered efficiently to users worldwide.

4. **Cost Efficiency**:
   - By offloading traffic from the origin server to the CDN, you can reduce bandwidth costs and server load.

5. **Security**:
   - Azure CDN provides enhanced security features such as DDoS protection, HTTPS, and custom domain support.

### Use Cases for Azure CDN

1. **Website Acceleration**:
   - Improve load times for websites by caching static assets like images, stylesheets, and JavaScript files.

2. **Video Streaming**:
   - Deliver smooth and high-quality video streaming experiences by caching video content closer to end-users.

3. **Software Distribution**:
   - Efficiently distribute software updates and downloads to users around the world.

4. **E-commerce**:
   - Enhance the user experience for online shopping by reducing latency and improving page load times.

### Setting Up Azure CDN

1. **Create a CDN Profile**:
   - In the Azure portal, create a CDN profile, which acts as a container for CDN endpoints.

2. **Create a CDN Endpoint**:
   - Within the CDN profile, create one or more CDN endpoints. Specify the origin server from which the CDN will pull content.

3. **Configure Caching Rules**:
   - Define caching rules to control how content is cached and served.

4. **Monitor and Manage**:
   - Use Azure Monitor and other tools to monitor performance, view analytics, and manage your CDN setup.

### Azure CDN Pricing

- Azure CDN pricing is based on several factors, including the amount of data transferred, the number of requests, and the geographic region. It is important to review the pricing details and plan according to your specific needs and usage patterns.

By leveraging Azure CDN, you can significantly improve the performance and scalability of your applications, ensuring a better experience for your users.

Sure, let's look at some detailed real-world examples of how Azure Content Delivery Network (CDN) is used across different industries:

### 1. E-commerce: Contoso Clothing

**Scenario**:
Contoso Clothing, a global e-commerce platform, sells fashion apparel and accessories. They experience high traffic, especially during sales and holiday seasons, which often leads to slow page load times and a poor user experience.

**Solution**:
Contoso Clothing integrates Azure CDN to cache their product images, JavaScript files, CSS files, and other static content. By doing this, they achieve:

- **Reduced Latency**: Customers accessing the website from different parts of the world experience faster load times as content is served from the nearest CDN POP.
- **Improved Scalability**: During peak times, such as Black Friday sales, Azure CDN handles the increased load, ensuring the site remains responsive.
- **Enhanced User Experience**: Faster page load times lead to higher customer satisfaction and potentially increased sales conversions.

### 2. Media & Entertainment: StreamFlix

**Scenario**:
StreamFlix, a video streaming service, provides high-definition video content to millions of users worldwide. They face challenges in delivering smooth streaming experiences due to bandwidth limitations and server load.

**Solution**:
StreamFlix employs Azure CDN to cache video content at edge locations. Key benefits include:

- **Smooth Streaming**: Video files are cached closer to users, reducing buffering times and improving playback quality.
- **Bandwidth Optimization**: By offloading the majority of data transfer to the CDN, StreamFlix reduces bandwidth costs and server load on their origin servers.
- **Global Reach**: Users from different regions can access content with minimal latency, ensuring a consistent viewing experience.

### 3. Software Distribution: SoftCo

**Scenario**:
SoftCo, a software development company, releases frequent updates for its applications. Distributing these updates to users across the globe can be challenging due to varying network conditions and server capacity.

**Solution**:
SoftCo leverages Azure CDN to distribute software updates efficiently. The CDN caches update files, providing:

- **Faster Downloads**: Updates are delivered from the nearest edge server, significantly reducing download times for users.
- **Scalability**: The CDN handles high traffic volumes during new release periods, ensuring reliable delivery.
- **Security**: SoftCo uses Azure CDN’s HTTPS support to securely distribute software updates, protecting users from potential threats.

### 4. Education: EduLearn

**Scenario**:
EduLearn, an online learning platform, provides educational videos, documents, and interactive content to students globally. They aim to deliver content efficiently to enhance the learning experience.

**Solution**:
EduLearn integrates Azure CDN to cache and deliver their educational content. The results are:

- **Enhanced Performance**: Educational videos and interactive content load faster, providing a seamless learning experience.
- **Global Accessibility**: Students from different regions can access content quickly, regardless of their location.
- **Cost Efficiency**: By reducing the load on origin servers, EduLearn optimizes operational costs while maintaining high performance.

### 5. News & Media: DailyNews

**Scenario**:
DailyNews, an online news portal, publishes real-time news articles, images, and videos. During major events, their site experiences a significant spike in traffic, leading to slow load times and potential outages.

**Solution**:
DailyNews implements Azure CDN to cache news articles, images, and videos at edge locations. This provides:

- **Improved Load Times**: Content is delivered quickly to users, enhancing the user experience.
- **High Availability**: The CDN handles traffic spikes efficiently, preventing server overload and ensuring continuous availability.
- **Dynamic Content Caching**: Azure CDN can be configured to cache frequently updated content, ensuring users receive the latest news with minimal delay.

### Summary

In each of these scenarios, Azure CDN helps organizations deliver content efficiently, reduce latency, improve user experience, and optimize costs. By leveraging Azure CDN’s global network of edge servers, businesses can ensure their content is accessible and performant for users around the world, regardless of traffic conditions or geographic location.


Sure, here is an example of how you can use Terraform to create and configure an Azure CDN endpoint. This example assumes that you have already set up your Terraform environment and have the necessary Azure provider configuration.

### Step 1: Configure the Azure Provider

First, ensure that you have the Azure provider configured. Create a file named `provider.tf`:

```hcl
provider "azurerm" {
  features {}
}
```

### Step 2: Create Resource Group and Storage Account

Create a file named `main.tf` to define your resource group and storage account:

```hcl
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_storage_account" "example" {
  name                     = "examplestoracc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

### Step 3: Create a CDN Profile

Extend the `main.tf` to include a CDN profile:

```hcl
resource "azurerm_cdn_profile" "example" {
  name                = "example-cdnprofile"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  sku                 = "Standard_Verizon"
}
```

### Step 4: Create a CDN Endpoint

Add the CDN endpoint to your `main.tf` file:

```hcl
resource "azurerm_cdn_endpoint" "example" {
  name                = "example-cdnendpoint"
  profile_name        = azurerm_cdn_profile.example.name
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  origin {
    name      = "example-origin"
    host_name = azurerm_storage_account.example.primary_blob_endpoint
  }
  is_http_allowed = true
  is_https_allowed = true
}
```

### Step 5: Output the CDN Endpoint URL

Optionally, you can create an output to display the CDN endpoint URL. Add this to your `main.tf`:

```hcl
output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.example.host_name
}
```

### Step 6: Initialize and Apply the Configuration

Run the following commands in your terminal:

```sh
terraform init
terraform apply
```

You will be prompted to confirm the action. Type `yes` to proceed. Terraform will then create the necessary resources, and you will see the CDN endpoint URL in the output.

### Summary

This Terraform script sets up an Azure CDN profile and endpoint, using a storage account as the origin. By using Terraform, you can manage and version control your infrastructure as code, making it easier to maintain and update over time.

Sure! Below are Terraform scripts tailored for real-world examples in various industries:

### Example 1: E-commerce (Contoso Clothing)

**Objective**: Cache static content (images, CSS, JavaScript) for a global e-commerce platform.

```hcl
# provider.tf
provider "azurerm" {
  features {}
}

# main.tf
resource "azurerm_resource_group" "ecommerce" {
  name     = "ecommerce-resources"
  location = "West Europe"
}

resource "azurerm_storage_account" "ecommerce" {
  name                     = "ecommercestoracc"
  resource_group_name      = azurerm_resource_group.ecommerce.name
  location                 = azurerm_resource_group.ecommerce.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_cdn_profile" "ecommerce" {
  name                = "ecommerce-cdnprofile"
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  sku                 = "Standard_Verizon"
}

resource "azurerm_cdn_endpoint" "ecommerce" {
  name                = "ecommerce-cdnendpoint"
  profile_name        = azurerm_cdn_profile.ecommerce.name
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  origin {
    name      = "ecommerce-origin"
    host_name = azurerm_storage_account.ecommerce.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralMediaStreaming"
}

output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.ecommerce.host_name
}
```

### Example 2: Media & Entertainment (StreamFlix)

**Objective**: Cache video content to improve streaming quality and reduce buffering.

```hcl
# provider.tf
provider "azurerm" {
  features {}
}

# main.tf
resource "azurerm_resource_group" "streamflix" {
  name     = "streamflix-resources"
  location = "West US"
}

resource "azurerm_storage_account" "streamflix" {
  name                     = "streamflixstoracc"
  resource_group_name      = azurerm_resource_group.streamflix.name
  location                 = azurerm_resource_group.streamflix.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_cdn_profile" "streamflix" {
  name                = "streamflix-cdnprofile"
  resource_group_name = azurerm_resource_group.streamflix.name
  location            = azurerm_resource_group.streamflix.location
  sku                 = "Premium_Verizon"
}

resource "azurerm_cdn_endpoint" "streamflix" {
  name                = "streamflix-cdnendpoint"
  profile_name        = azurerm_cdn_profile.streamflix.name
  resource_group_name = azurerm_resource_group.streamflix.name
  location            = azurerm_resource_group.streamflix.location
  origin {
    name      = "streamflix-origin"
    host_name = azurerm_storage_account.streamflix.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "VideoOnDemandMediaStreaming"
}

output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.streamflix.host_name
}
```

### Example 3: Software Distribution (SoftCo)

**Objective**: Efficiently distribute software updates globally.

```hcl
# provider.tf
provider "azurerm" {
  features {}
}

# main.tf
resource "azurerm_resource_group" "softco" {
  name     = "softco-resources"
  location = "East US"
}

resource "azurerm_storage_account" "softco" {
  name                     = "softcostoracc"
  resource_group_name      = azurerm_resource_group.softco.name
  location                 = azurerm_resource_group.softco.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_cdn_profile" "softco" {
  name                = "softco-cdnprofile"
  resource_group_name = azurerm_resource_group.softco.name
  location            = azurerm_resource_group.softco.location
  sku                 = "Standard_Microsoft"
}

resource "azurerm_cdn_endpoint" "softco" {
  name                = "softco-cdnendpoint"
  profile_name        = azurerm_cdn_profile.softco.name
  resource_group_name = azurerm_resource_group.softco.name
  location            = azurerm_resource_group.softco.location
  origin {
    name      = "softco-origin"
    host_name = azurerm_storage_account.softco.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralWebDelivery"
}

output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.softco.host_name
}
```

### Example 4: Education (EduLearn)

**Objective**: Cache educational videos and interactive content to enhance the learning experience.

```hcl
# provider.tf
provider "azurerm" {
  features {}
}

# main.tf
resource "azurerm_resource_group" "edulearn" {
  name     = "edulearn-resources"
  location = "Central US"
}

resource "azurerm_storage_account" "edulearn" {
  name                     = "edulearnstoracc"
  resource_group_name      = azurerm_resource_group.edulearn.name
  location                 = azurerm_resource_group.edulearn.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_cdn_profile" "edulearn" {
  name                = "edulearn-cdnprofile"
  resource_group_name = azurerm_resource_group.edulearn.name
  location            = azurerm_resource_group.edulearn.location
  sku                 = "Standard_Akamai"
}

resource "azurerm_cdn_endpoint" "edulearn" {
  name                = "edulearn-cdnendpoint"
  profile_name        = azurerm_cdn_profile.edulearn.name
  resource_group_name = azurerm_resource_group.edulearn.name
  location            = azurerm_resource_group.edulearn.location
  origin {
    name      = "edulearn-origin"
    host_name = azurerm_storage_account.edulearn.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralMediaStreaming"
}

output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.edulearn.host_name
}
```

### Example 5: News & Media (DailyNews)

**Objective**: Cache news articles, images, and videos to handle high traffic during major events.

```hcl
# provider.tf
provider "azurerm" {
  features {}
}

# main.tf
resource "azurerm_resource_group" "dailynews" {
  name     = "dailynews-resources"
  location = "East US 2"
}

resource "azurerm_storage_account" "dailynews" {
  name                     = "dailynewsstoracc"
  resource_group_name      = azurerm_resource_group.dailynews.name
  location                 = azurerm_resource_group.dailynews.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_cdn_profile" "dailynews" {
  name                = "dailynews-cdnprofile"
  resource_group_name = azurerm_resource_group.dailynews.name
  location            = azurerm_resource_group.dailynews.location
  sku                 = "Premium_Verizon"
}

resource "azurerm_cdn_endpoint" "dailynews" {
  name                = "dailynews-cdnendpoint"
  profile_name        = azurerm_cdn_profile.dailynews.name
  resource_group_name = azurerm_resource_group.dailynews.name
  location            = azurerm_resource_group.dailynews.location
  origin {
    name      = "dailynews-origin"
    host_name = azurerm_storage_account.dailynews.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralMediaStreaming"
}

output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.dailynews.host_name
}
```

### Summary

These Terraform scripts demonstrate how to set up Azure CDN for various use cases, including e-commerce, media streaming, software distribution, education, and news delivery. Each script configures an Azure Storage Account as the origin, creates a CDN profile, and sets up a CDN endpoint tailored to the specific requirements of the industry. Adjust the configurations according to your specific needs and infrastructure.


Certainly! Let's delve into the details of each Terraform script provided for the real-world examples.

### Example 1: E-commerce (Contoso Clothing)

**Objective**: Cache static content (images, CSS, JavaScript) for a global e-commerce platform.

#### provider.tf
```hcl
provider "azurerm" {
  features {}
}
```
This block configures the Azure provider, enabling Terraform to interact with Azure resources.

#### main.tf
```hcl
resource "azurerm_resource_group" "ecommerce" {
  name     = "ecommerce-resources"
  location = "West Europe"
}
```
- **azurerm_resource_group**: Defines a resource group named `ecommerce-resources` in the `West Europe` region.

```hcl
resource "azurerm_storage_account" "ecommerce" {
  name                     = "ecommercestoracc"
  resource_group_name      = azurerm_resource_group.ecommerce.name
  location                 = azurerm_resource_group.ecommerce.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **azurerm_storage_account**: Creates a storage account named `ecommercestoracc` within the resource group. It uses Standard performance tier and Locally Redundant Storage (LRS) for replication.

```hcl
resource "azurerm_cdn_profile" "ecommerce" {
  name                = "ecommerce-cdnprofile"
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  sku                 = "Standard_Verizon"
}
```
- **azurerm_cdn_profile**: Sets up a CDN profile named `ecommerce-cdnprofile` using the Verizon CDN tier.

```hcl
resource "azurerm_cdn_endpoint" "ecommerce" {
  name                = "ecommerce-cdnendpoint"
  profile_name        = azurerm_cdn_profile.ecommerce.name
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  origin {
    name      = "ecommerce-origin"
    host_name = azurerm_storage_account.ecommerce.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralMediaStreaming"
}
```
- **azurerm_cdn_endpoint**: Defines a CDN endpoint named `ecommerce-cdnendpoint`. It points to the storage account as the origin. Both HTTP and HTTPS are allowed, and the optimization type is set for general media streaming.

```hcl
output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.ecommerce.host_name
}
```
- **output**: Outputs the CDN endpoint URL after the infrastructure is deployed.

### Example 2: Media & Entertainment (StreamFlix)

**Objective**: Cache video content to improve streaming quality and reduce buffering.

#### provider.tf
```hcl
provider "azurerm" {
  features {}
}
```

#### main.tf
```hcl
resource "azurerm_resource_group" "streamflix" {
  name     = "streamflix-resources"
  location = "West US"
}
```
- **azurerm_resource_group**: Defines a resource group named `streamflix-resources` in the `West US` region.

```hcl
resource "azurerm_storage_account" "streamflix" {
  name                     = "streamflixstoracc"
  resource_group_name      = azurerm_resource_group.streamflix.name
  location                 = azurerm_resource_group.streamflix.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **azurerm_storage_account**: Creates a storage account named `streamflixstoracc` with standard performance and LRS replication.

```hcl
resource "azurerm_cdn_profile" "streamflix" {
  name                = "streamflix-cdnprofile"
  resource_group_name = azurerm_resource_group.streamflix.name
  location            = azurerm_resource_group.streamflix.location
  sku                 = "Premium_Verizon"
}
```
- **azurerm_cdn_profile**: Sets up a CDN profile named `streamflix-cdnprofile` using the Premium Verizon tier.

```hcl
resource "azurerm_cdn_endpoint" "streamflix" {
  name                = "streamflix-cdnendpoint"
  profile_name        = azurerm_cdn_profile.streamflix.name
  resource_group_name = azurerm_resource_group.streamflix.name
  location            = azurerm_resource_group.streamflix.location
  origin {
    name      = "streamflix-origin"
    host_name = azurerm_storage_account.streamflix.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "VideoOnDemandMediaStreaming"
}
```
- **azurerm_cdn_endpoint**: Creates a CDN endpoint named `streamflix-cdnendpoint` with the storage account as the origin. It allows both HTTP and HTTPS, optimized for video-on-demand media streaming.

```hcl
output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.streamflix.host_name
}
```
- **output**: Outputs the CDN endpoint URL.

### Example 3: Software Distribution (SoftCo)

**Objective**: Efficiently distribute software updates globally.

#### provider.tf
```hcl
provider "azurerm" {
  features {}
}
```

#### main.tf
```hcl
resource "azurerm_resource_group" "softco" {
  name     = "softco-resources"
  location = "East US"
}
```
- **azurerm_resource_group**: Defines a resource group named `softco-resources` in the `East US` region.

```hcl
resource "azurerm_storage_account" "softco" {
  name                     = "softcostoracc"
  resource_group_name      = azurerm_resource_group.softco.name
  location                 = azurerm_resource_group.softco.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **azurerm_storage_account**: Creates a storage account named `softcostoracc` with standard performance and LRS replication.

```hcl
resource "azurerm_cdn_profile" "softco" {
  name                = "softco-cdnprofile"
  resource_group_name = azurerm_resource_group.softco.name
  location            = azurerm_resource_group.softco.location
  sku                 = "Standard_Microsoft"
}
```
- **azurerm_cdn_profile**: Sets up a CDN profile named `softco-cdnprofile` using the Standard Microsoft tier.

```hcl
resource "azurerm_cdn_endpoint" "softco" {
  name                = "softco-cdnendpoint"
  profile_name        = azurerm_cdn_profile.softco.name
  resource_group_name = azurerm_resource_group.softco.name
  location            = azurerm_resource_group.softco.location
  origin {
    name      = "softco-origin"
    host_name = azurerm_storage_account.softco.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralWebDelivery"
}
```
- **azurerm_cdn_endpoint**: Creates a CDN endpoint named `softco-cdnendpoint` optimized for general web delivery.

```hcl
output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.softco.host_name
}
```
- **output**: Outputs the CDN endpoint URL.

### Example 4: Education (EduLearn)

**Objective**: Cache educational videos and interactive content to enhance the learning experience.

#### provider.tf
```hcl
provider "azurerm" {
  features {}
}
```

#### main.tf
```hcl
resource "azurerm_resource_group" "edulearn" {
  name     = "edulearn-resources"
  location = "Central US"
}
```
- **azurerm_resource_group**: Defines a resource group named `edulearn-resources` in the `Central US` region.

```hcl
resource "azurerm_storage_account" "edulearn" {
  name                     = "edulearnstoracc"
  resource_group_name      = azurerm_resource_group.edulearn.name
  location                 = azurerm_resource_group.edulearn.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **azurerm_storage_account**: Creates a storage account named `edulearnstoracc` with standard performance and LRS replication.

```hcl
resource "azurerm_cdn_profile" "edulearn" {
  name                = "edulearn-cdnprofile"
  resource_group_name = azurerm_resource_group.edulearn.name
  location            = azurerm_resource_group.edulearn.location
  sku                 = "Standard_Akamai"
}
```
- **azurerm_cdn_profile**: Sets up a CDN profile named `edulearn-cdnprofile` using the Standard Akamai tier.

```hcl
resource "azurerm_cdn_endpoint" "edulearn" {
  name                = "edulearn-cdnendpoint"
  profile_name        = azurerm_cdn_profile.edulearn.name
  resource_group_name = azurerm_resource_group.edulearn.name
  location            = azurerm_resource_group.edulearn.location


  origin {
    name      = "edulearn-origin"
    host_name = azurerm_storage_account.edulearn.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralMediaStreaming"
}
```
- **azurerm_cdn_endpoint**: Creates a CDN endpoint named `edulearn-cdnendpoint` optimized for general media streaming.

```hcl
output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.edulearn.host_name
}
```
- **output**: Outputs the CDN endpoint URL.

### Example 5: News & Media (DailyNews)

**Objective**: Cache news articles, images, and videos to handle high traffic during major events.

#### provider.tf
```hcl
provider "azurerm" {
  features {}
}
```

#### main.tf
```hcl
resource "azurerm_resource_group" "dailynews" {
  name     = "dailynews-resources"
  location = "East US 2"
}
```
- **azurerm_resource_group**: Defines a resource group named `dailynews-resources` in the `East US 2` region.

```hcl
resource "azurerm_storage_account" "dailynews" {
  name                     = "dailynewsstoracc"
  resource_group_name      = azurerm_resource_group.dailynews.name
  location                 = azurerm_resource_group.dailynews.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- **azurerm_storage_account**: Creates a storage account named `dailynewsstoracc` with standard performance and LRS replication.

```hcl
resource "azurerm_cdn_profile" "dailynews" {
  name                = "dailynews-cdnprofile"
  resource_group_name = azurerm_resource_group.dailynews.name
  location            = azurerm_resource_group.dailynews.location
  sku                 = "Premium_Verizon"
}
```
- **azurerm_cdn_profile**: Sets up a CDN profile named `dailynews-cdnprofile` using the Premium Verizon tier.

```hcl
resource "azurerm_cdn_endpoint" "dailynews" {
  name                = "dailynews-cdnendpoint"
  profile_name        = azurerm_cdn_profile.dailynews.name
  resource_group_name = azurerm_resource_group.dailynews.name
  location            = azurerm_resource_group.dailynews.location
  origin {
    name      = "dailynews-origin"
    host_name = azurerm_storage_account.dailynews.primary_blob_endpoint
  }
  is_http_allowed  = true
  is_https_allowed = true
  optimization_type = "GeneralMediaStreaming"
}
```
- **azurerm_cdn_endpoint**: Creates a CDN endpoint named `dailynews-cdnendpoint` optimized for general media streaming.

```hcl
output "cdn_endpoint_url" {
  value = azurerm_cdn_endpoint.dailynews.host_name
}
```
- **output**: Outputs the CDN endpoint URL.

### Summary

Each script includes:
1. **Provider Configuration**: Ensures Terraform can interact with Azure resources.
2. **Resource Group**: Creates a resource group to hold all related resources.
3. **Storage Account**: Sets up a storage account as the origin for the CDN.
4. **CDN Profile**: Configures a CDN profile to manage CDN endpoints.
5. **CDN Endpoint**: Defines a CDN endpoint pointing to the storage account and configures optimization settings for specific use cases.
6. **Output**: Outputs the URL of the CDN endpoint for easy reference.

These scripts provide a foundational setup for leveraging Azure CDN across different industries, ensuring efficient content delivery and improved user experiences.


