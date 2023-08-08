#!/bin/bash

if [ "$3" = "avail" ]; then

  if [ "$4" = "cluster/" ]; then
    cat ${MOCK_FILE_AVAIL_CLUSTER} >&2
  else
    cat ${MOCK_FILE_AVAIL} >&2
  fi
else
  exit 1
fi
