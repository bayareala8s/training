.PHONY: help bootstrap init plan apply destroy validate fmt lab-start lab-stop lab-status

ENV ?= dev
LAB_DIR := labs/shared/environments/$(ENV)
BOOTSTRAP_DIR := labs/week-01/bootstrap
AWS_SCRIPTS := scripts/aws

help:
	@echo "BayAreaLa8s Terraform Enterprise Course"
	@echo ""
	@echo "  make bootstrap     - Create S3 + DynamoDB state backend"
	@echo "  make init ENV=dev  - terraform init with backend.hcl"
	@echo "  make plan ENV=dev"
	@echo "  make apply ENV=dev"
	@echo "  make destroy ENV=dev"
	@echo "  make validate      - fmt + validate all environments"
	@echo "  make lab-start     - Start tagged AWS lab resources"
	@echo "  make lab-stop      - Stop tagged AWS lab resources"
	@echo "  make lab-status    - Show lab resource status"

bootstrap:
	cd $(BOOTSTRAP_DIR) && terraform init && terraform apply

init:
	@test -f $(LAB_DIR)/backend.hcl || (echo "Copy backend.hcl.example to backend.hcl" && exit 1)
	cd $(LAB_DIR) && terraform init -backend-config=backend.hcl

plan:
	cd $(LAB_DIR) && terraform plan -var-file=terraform.tfvars

apply:
	cd $(LAB_DIR) && terraform apply -var-file=terraform.tfvars

destroy:
	cd $(LAB_DIR) && terraform destroy -var-file=terraform.tfvars

fmt:
	terraform fmt -recursive modules labs

validate: fmt
	@for env in dev test prod; do \
	  echo "=== Validating $$env ==="; \
	  cd labs/shared/environments/$$env && terraform init -backend=false && terraform validate && cd -; \
	done

lab-start:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/start-lab.sh

lab-stop:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/stop-lab.sh

lab-status:
	chmod +x $(AWS_SCRIPTS)/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/status-lab.sh

lab-verify:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/verify-labs.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/verify-labs.sh validate

lab-teardown:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/teardown-all.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/teardown-all.sh
