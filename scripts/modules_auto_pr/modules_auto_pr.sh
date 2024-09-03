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
REPO_PATH="$VSC_SCRATCH/modules_auto_pr_script_$DATE/$REPO_NAME"
COMMIT_MESSAGE="Update Modules"
PR_TITLE="Auto Update Modules"

make_pr_body() {
  local n_added_modules="$1"
  local n_removed_modules="$2"

  echo "This is an automated pull request updating the markdown files of all available modules."
  echo ""
  echo "Changes:"
  echo "- Updated the markdown files of all previously available modules"
  echo "- Added $n_added_modules new modules"
  echo "- Removed $n_removed_modules modules"
}

####################################################################################################
#                                             SCRIPT                                               #
####################################################################################################

echo_info()  { echo -e "\e[32m$0: [INFO] $1\e[0m"; }
echo_error() { echo -e "\e[31m$0: [ERROR] $1\e[0m"; }

main() {
  local github_pat_file="$1"

  gh auth login --with-token < "$github_pat_file"

  # Check if the repo directory already exists. If so, ask user to delete it.
  if [ -d "$REPO_PATH" ]; then
      echo_error "Directory $REPO_PATH already exists."
      echo_error "Please remove it manually:"
      echo_error "  $ rm -rf $REPO_PATH"
      exit 1
  fi

  # Clone the repository and create a new branch
  git clone $REPO_URL "$REPO_PATH"
  cd "$REPO_PATH"
  git checkout -b "$BRANCH_NAME"

  # run available_software.py
  python -m venv venv
  source venv/bin/activate
  pip install -r scripts/available_software/requirements.txt
  python scripts/available_software/available_software.py

  # Add and commit the generated files
  git add .
  git commit -m "$COMMIT_MESSAGE"

  # Calculate the number of added and removed modules
  N_ADDED_MODULES=$(git show --name-status HEAD | grep -e "^A.*\.md$" | wc -l)
  N_REMOVED_MODULES=$(git show --name-status HEAD | grep -e "^D.*\.md$" | wc -l)

  # Push the new branch to GitHub
  gh repo set-default $REPO_URL
  git push -u origin "$BRANCH_NAME"

  # Create a pull request using GitHub CLI
  gh pr create \
    --title "$PR_TITLE" \
    --body  "$(make_pr_body "$N_ADDED_MODULES" "$N_REMOVED_MODULES")" \
    --base  "$BASE_BRANCH" \
    --head  "$BRANCH_NAME" \

  # Clean up
  rm -rf "$REPO_PATH"
}

main "$1"