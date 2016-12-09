#!/bin/bash

set -e

echo "Preparing to deploy"

cd $HOME/build
mkdir pdf
mv *.pdf pdf

REPO_NAME=${GITHUB_REPO#*/}
GITHUB_USER=${GITHUB_REPO%/*}

wget https://${GITHUB_USER}.github.io/${REPO_NAME}/index.html
wget https://${GITHUB_USER}.github.io/${REPO_NAME}/tablesort.min.js

# Take the values from the Makefile and replace them in the HTML file
all_os=$(sed -n "s:^all_os\s*=\s*\(.*\)$:\1:p" $TRAVIS_BUILD_DIR/Makefile)
all_site=$(sed -n "s:^all_site\s*=\s*\(.*\)$:\1:p" $TRAVIS_BUILD_DIR/Makefile)
all_doc_os=$(sed -n "s:^all_doc_os\s*=\s*\(.*\)$:\1:p" $TRAVIS_BUILD_DIR/Makefile)
all_doc_noos=$(sed -n "s:^all_doc_noos\s*=\s*\(.*\)$:\1:p" $TRAVIS_BUILD_DIR/Makefile)

sed -i "s:^\s*var sites = \[.*$:var sites = \[\"${all_site// /\",\"}\"\];:" index.html
sed -i "s:^\s*var sysos = \[.*$:var sysos = \[\"${all_os// /\",\"}\"\];:" index.html
sed -i "s:^\s*var docsos = \[.*$:var docsos = \[\"${all_doc_os// /\",\"}\"\];:" index.html
sed -i "s:^\s*var docsnoos = \[.*$:var docsnoos = \[\"${all_doc_noos// /\",\"}\"\];:" index.html

git config --global user.email "hpc@ugent.be"
git config --global user.name "HPC UGent"

git init
git add ./pdf/*.pdf
git add index.html tablesort.min.js
git status
git commit -m "Deploy to Github Pages"
git push --force "https://${GH_TOKEN}@github.com/${GITHUB_REPO}.git" master:gh-pages
