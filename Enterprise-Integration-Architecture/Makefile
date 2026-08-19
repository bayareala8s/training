.PHONY: player validate fmt
player:
	python3 -m http.server 8080
validate:
	python3 scripts/validate_lab.py lab-01-classification || true
fmt:
	terraform fmt -recursive terraform/labs
