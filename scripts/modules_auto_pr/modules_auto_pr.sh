#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

####################################################################################################
#                                            VARIABLES                                             #
####################################################################################################

# Variables (replace these with your actual values)
DATE=$(date +"%Y-%m-%d_%Hh%M")
REPO_URL="git@github.com:lbarraga/vsc_user_docs.git"
BASE_BRANCH="main"
BRANCH_NAME="auto_update_modules_$DATE"
REPO_NAME="vsc_user_docs" # script available_modules.py requires this to be the name. Do not change.
REPO_PATH="/tmp/modules_auto_pr_script_$DATE/$REPO_NAME"
COMMIT_MESSAGE="Update Modules"
PR_TITLE="Auto Update Modules"
make_pr_body() {
  local n_added_modules="$1"
  local n_removed_modules="$2"

  echo "This is an automated pull request to update the markdown files of all available modules."
  echo ""
  echo "Changes:"
  echo "- Updated the markdown files of all previously available modules"
  echo "- Added $n_added_modules new modules"
  echo "- Removed $n_removed_modules modules"
}

# Use GitHub CLI for authentication
GH_TOKEN="SAMPLE_TOKEN" # Test token, will not be used in production

echo_info()    { echo -e "\e[32m$0: [INFO] $1\e[0m"; }
echo_warning() { echo -e "\e[33m$0: [WARNING] $1\e[0m"; }
echo_error()   { echo -e "\e[31m$0: [ERROR] $1\e[0m"; }

####################################################################################################
#                                             SCRIPT                                               #
####################################################################################################

echo_info "Logging in to GitHub..."
gh auth login --with-token <<< "$GH_TOKEN"

# Check if the repo directory already exists and delete it if so
if [ -d "$REPO_PATH" ]; then
    echo_error "Directory $REPO_PATH already exists."
    echo_error "Please remove it manually:"
    echo_error "  $ rm -rf $REPO_PATH"
    exit 1
fi

echo_info "Cloning repo $REPO_URL..."
git clone $REPO_URL "$REPO_PATH"

echo_info "Navigating to repo directory..."
cd "$REPO_PATH"

echo_info "Checking out base branch $BASE_BRANCH..."
git checkout -b "$BRANCH_NAME"

# run available_software.py
echo_info "Running available_software.py..."
cd scripts/available_software/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python available_software.py

# Add and commit the new file
echo_info "Adding and committing the new files..."
cd "$REPO_PATH"
git add .
git commit -m "$COMMIT_MESSAGE"

# Calculate the number of added and removed modules
N_ADDED_MODULES=$(git show --name-status HEAD | grep -c "^A.*\.md$")
N_REMOVED_MODULES=$(git show --name-status HEAD | grep -c "^D.*\.md$")

# Push the new branch to GitHub
echo_info "Pushing branch to GitHub..."
git push -u origin "$BRANCH_NAME"

echo_info "Setting default repo..."
gh repo set-default $REPO_URL

# Create a pull request using GitHub CLI
echo_info "Creating a pull request..."
gh pr create \
  --title "$PR_TITLE" \
  --body  "$(make_pr_body "$N_ADDED_MODULES" "$N_REMOVED_MODULES")" \
  --base  "$BASE_BRANCH" \
  --head  "$BRANCH_NAME" \

# Clean up
rm -rf "$REPO_PATH"
