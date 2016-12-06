#!/bin/bash

set -e

echo "Preparing to deploy"

cd $HOME/build
mkdir pdf
mv *.pdf pdf

git config --global user.email "hpc@ugent.be"
git config --global user.name "HPC UGent"

git init
git add ./pdf/*.pdf
git status
git commit -m "Deploy to Github Pages"
git push --force "https://${GH_TOKEN}@github.com/${GITHUB_REPO}.git" master:gh-pages
