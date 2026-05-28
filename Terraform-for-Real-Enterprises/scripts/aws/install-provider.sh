#!/usr/bin/env bash
# Install hashicorp/aws provider locally when Terraform registry query fails.
# Usage: ./install-provider.sh [version]
set -euo pipefail

VERSION="${1:-5.90.0}"
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"
[[ "$ARCH" == "x86_64" ]] && ARCH="amd64"
[[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]] && ARCH="arm64"

PLUGIN_ROOT="/tmp/tf-plugins"
TARGET="${PLUGIN_ROOT}/registry.terraform.io/hashicorp/aws/${VERSION}/${OS}_${ARCH}"

mkdir -p "${TARGET}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading terraform-provider-aws ${VERSION} for ${OS}_${ARCH}..."
curl -fsSL -o "${TMP}/provider.zip" \
  "https://releases.hashicorp.com/terraform-provider-aws/${VERSION}/terraform-provider-aws_${VERSION}_${OS}_${ARCH}.zip"
unzip -qo "${TMP}/provider.zip" -d "${TMP}"
install -m 755 "${TMP}"/terraform-provider-aws_* "${TARGET}/"

cat > /tmp/terraform-lab.rc <<EOF
provider_installation {
  filesystem_mirror {
    path    = "${PLUGIN_ROOT}"
    include = ["registry.terraform.io/hashicorp/*"]
  }
  direct {
    exclude = ["registry.terraform.io/hashicorp/*"]
  }
}
EOF

echo "Installed to ${TARGET}"
echo "Run: export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc"
echo "Then: terraform init"
