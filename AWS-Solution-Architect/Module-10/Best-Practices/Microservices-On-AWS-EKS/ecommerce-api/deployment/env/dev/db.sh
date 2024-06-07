#!/bin/bash

#./db.sh us-west-2 ecommerce youruser yourpassword ecommerce

# Set variables
AWS_REGION=$1
DB_INSTANCE_IDENTIFIER=$2
MASTER_USERNAME=$3
MASTER_PASSWORD=$4
# Set the DB name
DB_NAME=$5

# Get the default VPC
DEFAULT_VPC_ID=$(aws ec2 describe-vpcs --filter "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text --region $AWS_REGION)

# Get the Subnet IDs of the default VPC
SUBNET_IDS=$(aws ec2 describe-subnets --filter "Name=vpc-id,Values=$DEFAULT_VPC_ID" --query "Subnets[*].SubnetId" --output text --region $AWS_REGION)

# Create a DB Subnet Group
aws rds create-db-subnet-group --db-subnet-group-name ecom-app-dev-postgresqldb-subnetgroup --subnet-ids $SUBNET_IDS --db-subnet-group-description "ECOM App PostgreSQL DB subnet group" --region $AWS_REGION

# Create a PostgreSQL DB instance
aws rds create-db-instance --db-instance-identifier $DB_INSTANCE_IDENTIFIER --db-instance-class db.t3.micro --engine postgres --engine-version 16.2 --master-username $MASTER_USERNAME --master-user-password $MASTER_PASSWORD --allocated-storage 20 --db-subnet-group-name ecom-app-dev-postgresqldb-subnetgroup --region $AWS_REGION

# Wait for the DB instance to become available
aws rds wait db-instance-available --db-instance-identifier $DB_INSTANCE_IDENTIFIER --region $AWS_REGION

# Create a database
aws rds create-db-instance --db-instance-identifier $DB_INSTANCE_IDENTIFIER --db-name $DB_NAME --region $AWS_REGION