#!/bin/bash

set -e

echo "Preparing to deploy"

# Take the values from the Makefile and replace them in the HTML file
all_os=$(sed -n "s:^all_os\s*=\s*\(.*\)$:\1:p" Makefile)
all_site=$(sed -n "s:^all_site\s*=\s*\(.*\)$:\1:p" Makefile)
all_doc_os=$(sed -n "s:^all_doc_os\s*=\s*\(.*\)$:\1:p" Makefile)
all_doc_noos=$(sed -n "s:^all_doc_noos\s*=\s*\(.*\)$:\1:p" Makefile)

sed -i "s:^\s*var sites = \[.*$:var sites = \[\"${all_site// /\",\"}\"\];:" web/index.html
sed -i "s:^\s*var sysos = \[.*$:var sysos = \[\"${all_os// /\",\"}\"\];:" web/index.html
sed -i "s:^\s*var docsos = \[.*$:var docsos = \[\"${all_doc_os// /\",\"}\"\];:" web/index.html
sed -i "s:^\s*var docsnoos = \[.*$:var docsnoos = \[\"${all_doc_noos// /\",\"}\"\];:" web/index.html
