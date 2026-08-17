.PHONY: install start build lint spell validate ci clean help aws-setup aws-deploy aws-status aws-domain generate-stripe-aws-pngs

help:
	@echo "Principal Architect Knowledge System"
	@echo ""
	@echo "  make install     - Install Node and Python dependencies"
	@echo "  make start       - Start Docusaurus dev server"
	@echo "  make build       - Build documentation site"
	@echo "  make aws-setup   - Create S3 + CloudFront stack (one-time)"
	@echo "  make aws-deploy  - Build and deploy portal to AWS"
	@echo "  make aws-domain  - Attach custom domain (e.g. paks.bayareala8s.com)"
	@echo "  make aws-status  - Show deployed portal URL"
	@echo "  make generate-stripe-aws-pngs - AWS Architecture Icons PNGs (Stripe idempotency)"
	@echo "  make lint        - Run Markdown and ESLint checks"
	@echo "  make spell       - Run spelling checks"
	@echo "  make validate    - Validate metadata, links, and coverage"
	@echo "  make ci          - Run full CI pipeline locally"
	@echo "  make clean       - Remove build artifacts"

install:
	npm install
	@test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -q pytest pyyaml 2>/dev/null || true

start:
	npm start

serve:
	npm run build && npm run serve

build:
	npm run build

lint:
	npm run lint

spell:
	npm run spell

validate:
	npm run validate

validate-diagrams:
	python3 scripts/validate_mermaid.py

ensure-diagrams:
	python3 scripts/ensure_diagrams.py

build-flashcards:
	python3 scripts/build_flashcards.py

test-labs:
	@for lab in labs/lab-001-* labs/lab-002-* labs/lab-005-* labs/lab-006-* labs/lab-008-* labs/lab-009-* labs/lab-011-* labs/lab-014-* labs/lab-015-* labs/lab-016-* labs/lab-017-*; do \
		echo "Testing $$lab (python)..."; \
		(cd $$lab && ../../.venv/bin/python -m pytest tests/ -q) || exit 1; \
	done
	@for lab in labs/lab-003-* labs/lab-004-* labs/lab-007-* labs/lab-010-* labs/lab-013-*; do \
		echo "Testing $$lab (go)..."; \
		(cd $$lab && GOTOOLCHAIN=local go test -timeout 30s ./... -count=1) || exit 1; \
	done

ci:
	npm run ci

aws-setup:
	chmod +x scripts/setup-aws-infrastructure.sh scripts/deploy-aws.sh scripts/setup-custom-domain.sh
	./scripts/setup-aws-infrastructure.sh

aws-domain:
	chmod +x scripts/setup-custom-domain.sh
	@test -n "$$CUSTOM_DOMAIN" || (echo "Usage: CUSTOM_DOMAIN=paks.bayareala8s.com HOSTED_ZONE_NAME=bayareala8s.com make aws-domain" && exit 1)
	./scripts/setup-custom-domain.sh

aws-deploy:
	chmod +x scripts/deploy-aws.sh
	./scripts/deploy-aws.sh

aws-status:
	@test -f deploy/aws.env && . deploy/aws.env && echo "Portal URL: $$SITE_URL" && echo "CloudFront:  $${CLOUDFRONT_URL:-n/a}" || echo "Run: make aws-setup"

generate-stripe-aws-pngs:
	@test -d .venv-diagrams || python3 -m venv .venv-diagrams
	.venv-diagrams/bin/pip install -q -r scripts/requirements-diagrams.txt
	.venv-diagrams/bin/python scripts/inject_stripe_diagram_steps.py
	.venv-diagrams/bin/python scripts/generate_stripe_aws_architecture_pngs.py

clean:
	rm -rf node_modules build .docusaurus
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
