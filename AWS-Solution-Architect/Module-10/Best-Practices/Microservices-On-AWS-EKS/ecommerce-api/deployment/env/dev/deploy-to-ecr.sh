#!/bin/bash

#./deploy-to-ecr.sh us-west-2 277374794397 ecommerce-api

# This script deploys a Docker image to an Amazon Elastic Container Registry (ECR) repository.

# Replace these variables with your own values
AWS_REGION=$1
AWS_ACCOUNT_ID=$2
DOCKER_IMAGE_TAG=$3

# Get all tags for the specified image name
tags=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "^$3:" | awk -F':' '{print $2}')

# Check if tags are available
if [ -z "$tags" ]; then
    echo "No tags found for image: $3"
    exit 1
fi

# Print the list of tags
echo "Tags for image $3:"
echo "$tags"

# Authenticate Docker client with ECR
$(aws ecr get-login --no-include-email --region $AWS_REGION)

# Create an ECR repository
ECR_REPO_NAME="ecommerce-api"
aws ecr create-repository --repository-name $ECR_REPO_NAME --region us-west-2

# Tag the Docker image
docker tag $DOCKER_IMAGE_TAG:$tags $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DOCKER_IMAGE_TAG:$tags

sleep 5

# Push the Docker image to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DOCKER_IMAGE_TAG:$tags

echo "Docker image $DOCKER_IMAGE_TAG:$tags deployed to ECR repository $ECR_REPO_NAME"
