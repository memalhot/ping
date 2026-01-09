#!/bin/bash

oc project mm-pingtest

for i in $(seq 1 10); do
  NOTEBOOK_NAME="notebook-$i"
  PVC_NAME="notebook-pvc-$i"

  oc ${OC_ARGS} delete notebook "${NOTEBOOK_NAME}" --as system:admin --ignore-not-found

  oc ${OC_ARGS} delete pvc "${PVC_NAME}" --as system:admin --ignore-not-found
done