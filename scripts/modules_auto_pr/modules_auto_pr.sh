#!/bin/bash

####################################################################################################
#                                            VARIABLES                                             #
####################################################################################################

# Variables (replace these with your actual values)
DATE=$(date +"%Y-%m-%d_%Hh%M")
REPO_URL="git@github.com:lbarraga/token-test.git"
BASE_BRANCH="main"
BRANCH_NAME="new-feature-branch_$DATE"
REPO_NAME="token-test_$DATE"
REPO_PATH="/tmp/$REPO_NAME"
FILE_NAME="newfile.txt"
COMMIT_MESSAGE="Add newfile.txt"
PR_TITLE="Add new file as part of feature"
PR_BODY="This PR adds a new file to the repository."

# Use GitHub CLI for authentication
GH_TOKEN="SAMPLE_TOKEN" # Test token, will not be used in production

echo_info()    { echo -e "\e[32m$0: [INFO] $1\e[0m"; }
echo_warning() { echo -e "\e[33m$0: [WARNING] $1\e[0m"; }
echo_error()   { echo -e "\e[31m$0: [ERROR] $1\e[0m"; }

####################################################################################################
#                                             SCRIPT                                               #
####################################################################################################

echo_info "Logging in to GitHub..."
gh auth login --with-token <<< "$GH_TOKEN" || { echo_error "Failed to log in to GitHub"; exit 1; }

# Check if the repo directory already exists and delete it if so
if [ -d "$REPO_PATH" ]; then
    echo_error "Directory $REPO_PATH already exists."
    echo_error "Please remove it manually:"
    echo_error "  $ rm -rf $REPO_PATH"
    exit 1
fi

echo_info "Cloning repo $REPO_URL..."
git clone $REPO_URL "$REPO_PATH" || { echo_error "Failed to clone repo $REPO_URL"; exit 1; }

echo_info "Navigating to repo directory..."
cd "$REPO_PATH" || { echo_error "Failed to cd into $REPO_PATH"; exit 1; }

echo_info "Checking out base branch $BASE_BRANCH..."
git checkout -b "$BRANCH_NAME" || { echo_error "Failed to create branch $BRANCH_NAME"; exit 1; }

# run available_software.py
cd scripts/available_software/  || { echo_error "Failed to cd into scripts/available_software/"; exit 1; }
python -m venv venv             || { echo_error "Failed to create virtual environment"; exit 1; }
source venv/bin/activate        || { echo_error "Failed to activate virtual environment"; exit 1; }
pip install requests            || { echo_error "Failed to install requests"; exit 1; }
python available_software.py    || { echo_error "Failed to run available_software.py"; exit 1; }

# Add and commit the new file
echo_info "Adding and committing the new files..."
cd "$REPO_PATH"                 || { echo_error "Failed to cd into $REPO_PATH"; exit 1; }
git add .                       || { echo_error "Failed to add files"; exit 1; }
git commit -m "$COMMIT_MESSAGE" || { echo_error "Failed to commit changes"; exit 1; }

# Push the new branch to GitHub
echo_info "Pushing branch to GitHub..."
git push -u origin "$BRANCH_NAME" || { echo_error "Failed to push branch $BRANCH_NAME"; exit 1; }

# Create a pull request using GitHub CLI
echo_info "Creating a pull request..."
gh pr create \
  --title "$PR_TITLE" \
  --body  "$PR_BODY" \
  --base  "$BASE_BRANCH" \
  --head  "$BRANCH_NAME" \
  || { echo_error "Failed to create pull request"; exit 1; }

# Clean up
rm -rf "$REPO_PATH" || echo_warning "Failed to remove $REPO_PATH"
