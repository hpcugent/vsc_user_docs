#!/bin/bash

set -e

echo "Preparing to deploy"

cd $HOME/build
ls

git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

git init
git add ./*.pdf
git status
git commit -m "Deploy to Github Pages"
git log
git push --force "https://${GH_TOKEN}@github.com/${GITHUB_REPO}.git" master:gh-pages
