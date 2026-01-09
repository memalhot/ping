#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="mm-pingtest"

NB_TEMPLATE="nb.yaml"
PVC_TEMPLATE="pvc.yaml"

RUN_NAME="playwrite-test"
USER_NAME="memalhot"
IMAGE_NAME="ucsls-f24"
IMAGE_REPO="image-registry.openshift-image-registry.svc:5000/redhat-ods-applications"
PVC_SIZE="20Gi"
OPENSHIFT_URL="https://rhods-dashboard-redhat-ods-applications.apps.ocp-test.nerc.mghpcc.org/projects"
HUB_HOST="https://rhods-dashboard-redhat-ods-applications.apps.ocp-test.nerc.mghpcc.org"
TOKEN=""

oc project "${NAMESPACE}"

for i in $(seq 1 10); do
  NOTEBOOK_NAME="notebook-${i}"
  PVC_NAME="${NOTEBOOK_NAME}"   # IMPORTANT: matches claimName in nb.yaml

  echo "Applying PVC + Notebook for ${NOTEBOOK_NAME} (PVC=${PVC_NAME})..."

  # 1) PVC
  oc process --as system:admin -f "${PVC_TEMPLATE}" \
    -p PVC_NAME="${PVC_NAME}" \
    -p NAMESPACE="${NAMESPACE}" \
    -p PVC_SIZE="${PVC_SIZE}" \
    -p RUN_NAME="${RUN_NAME}" \
    -p USER="${USER_NAME}" \
  | oc apply -f -

  # 2) Notebook
  oc process --as system:admin -f "${NB_TEMPLATE}" \
    -p NOTEBOOK_NAME="${NOTEBOOK_NAME}" \
    -p RUN_NAME="${RUN_NAME}" \
    -p USERNAME="${USER_NAME}" \
    -p IMAGE_NAME="${IMAGE_NAME}" \
    -p NAMESPACE="${NAMESPACE}" \
    -p OPENSHIFT_URL="${OPENSHIFT_URL}" \
    -p USER="${USER_NAME}" \
    -p IMAGE_REPO="${IMAGE_REPO}" \
    -p HUB_HOST="${HUB_HOST}" \
    -p PVC_SIZE="${PVC_SIZE}" \
    -p TOKEN="${TOKEN}" \
  | oc apply -f -
done
