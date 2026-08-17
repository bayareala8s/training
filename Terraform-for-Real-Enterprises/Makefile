.PHONY: help bootstrap init plan apply destroy validate fmt fmt-check lab-start lab-stop lab-status lab-pause lab-resume lab-cycle lab-verify lab-teardown

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
	@echo "  make validate      - fmt-check + validate all environments (no file changes)"
	@echo "  make fmt           - format Terraform files (writes changes)"
	@echo "  make lab-pause     - Stop compute + destroy NAT GW (near-zero cost)"
	@echo "  make lab-resume    - Recreate NAT GW + start compute"
	@echo "  make lab-cycle     - Test pause then resume"
	@echo "  make lab-start     - Start tagged AWS lab resources"
	@echo "  make lab-stop      - Stop tagged AWS lab resources"
	@echo "  make lab-status    - Show lab resource status"
	@echo "  make lab-verify    - Terraform validate smoke test"
	@echo "  make lab-teardown  - Stop + destroy dev stack"

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

fmt-check:
	terraform fmt -check -recursive modules labs

validate: fmt-check
	@for env in dev test prod; do \
	  echo "=== Validating $$env ==="; \
	  cd labs/shared/environments/$$env && terraform init -backend=false -input=false && terraform validate && cd -; \
	done
	@echo "=== Validating bootstrap ==="
	@cd labs/week-01/bootstrap && terraform init -backend=false -input=false && terraform validate

lab-start:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/start-lab.sh

lab-stop:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/stop-lab.sh

lab-status:
	chmod +x $(AWS_SCRIPTS)/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/status-lab.sh

lab-pause:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/pause-labs.sh

lab-resume:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/resume-labs.sh

lab-cycle:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/lib/*.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/cycle-labs.sh

lab-verify:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/verify-labs.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/verify-labs.sh validate

lab-teardown:
	chmod +x $(AWS_SCRIPTS)/*.sh $(AWS_SCRIPTS)/teardown-all.sh 2>/dev/null || true
	$(AWS_SCRIPTS)/teardown-all.sh
