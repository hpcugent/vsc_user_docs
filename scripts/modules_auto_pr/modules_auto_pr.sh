#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed
set -u  # Treat unset variables as an error when substituting

####################################################################################################
#                                            VARIABLES                                             #
####################################################################################################

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
HUMAN_TIMESTAMP=$(date "+%-d %B %Y, %H:%M")
REPO_URL="git@github.com:hpcugent/vsc_user_docs.git"
BASE_BRANCH="main"
BRANCH_NAME="auto_update_modules_$TIMESTAMP"
REPO_NAME="vsc_user_docs" # script available_modules.py requires this to be the name. Do not change.
REPO_PATH="/tmp/$VSC_USER/modules_auto_pr_script_$TIMESTAMP/$REPO_NAME"
COMMIT_MESSAGE="Update Modules [$HUMAN_TIMESTAMP]"
PR_TITLE="Auto Update Modules [$HUMAN_TIMESTAMP]"

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

  # Check if the `gh` command is available
  if ! command -v gh &> /dev/null; then
      echo_error "The GitHub CLI (gh) is not installed."
      echo_error "Please install it by following the instructions at https://cli.github.com."
      exit 1
  fi

  # Check if the GitHub Personal Access Token file exists
  if [ ! -f "$github_pat_file" ]; then
      echo_error "GitHub Personal Access Token file not found."
      echo_error "Please provide the path to the file containing the GitHub Personal Access Token."
      echo_error "Usage: $0 <github_pat_file>"
      exit 1
  fi

  gh auth login --with-token < "$github_pat_file"

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