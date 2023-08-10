#!/bin/bash

# Emulated avail command.
if [ "$3" = "avail" ]; then
  if [ "$4" = "cluster/" ]; then
    cat "${MOCK_FILE_AVAIL_CLUSTER}" >&2
  else
    cat "${MOCK_FILE_AVAIL}" >&2
  fi


# Emulated swap command.
elif [ "$3" = "swap" ]; then
  #extract te cluster name from the 4th argument
  cluster=$(echo "$4" | cut -d "/" -f 1)
  cluster_name=$(echo "$4" | cut -d "/" -f 2)

  if [ "$cluster" = "cluster" ]; then
    # Substitute CLUSTER by the cluster_name
    echo "${MOCK_FILE_SWAP}" | sed "s/CLUSTER/${cluster_name}/" | xargs cat >&1
  else
    echo "Something is wrong"
    exit 1
  fi


else
  echo "Not supported"
  exit 1
fi
