#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error when substituting

####################################################################################################
#                                            VARIABLES                                             #
####################################################################################################

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
HUMAN_TIMESTAMP=$(date "+%-d %B %Y, %H:%M")
REPO_URL="git@github.com:hpcugent/vsc_user_docs" # The repository for which the script will generate the PR
BASE_BRANCH="main"
BRANCH_NAME="auto_update_modules_$TIMESTAMP"
REPO_NAME="vsc_user_docs" # name of the cloned repo. script available_modules.py requires this to be the name. Do not change.
REPO_PATH="/tmp/$USER/modules_auto_pr_script_$TIMESTAMP/$REPO_NAME"
COMMIT_MESSAGE="Update Modules [$HUMAN_TIMESTAMP]"
PR_TITLE="Auto Update Modules [$HUMAN_TIMESTAMP]"

make_pr_body() {
  local n_added_modules="$1"
  local n_removed_modules="$2"
  local n_modified_modules="$3"

  echo "This is an automated pull request updating the markdown files of all available modules."
  echo ""
  echo "Changes:"
  echo "- Updated $n_modified_modules modules"
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
  local fork_user="$2" # The user that owns the fork from which the script will create the PR. e.g. lbarraga
  local fork_url="git@github.com:$fork_user/vsc_user_docs" # The fork from which the script will create the PR

  # Check if the `gh` command is available
  if ! command -v gh &> /dev/null; then
      echo_error "The GitHub CLI (gh) is not installed."
      echo_error "Please install it by following the instructions at https://cli.github.com."
      exit 1
  fi

  # Check if PAT file is present and fork user is provided in one if statement
  # -s checks whether file exists and has non-zero size (is not empty)
  if [ ! -s "$github_pat_file" ] || [ -z "$fork_user" ]; then
      echo_error "Please provide a valid GitHub Personal Access Token (PAT) file and fork user."
      echo_error "Usage: $0 <github_pat_file> <fork_user>"
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
  N_MODIFIED_MODULES=$(git show --name-status HEAD | grep -e "^M.*\.md$" | wc -l)

  # Push the new branch to GitHub
  git remote add fork "$fork_url"
  git push fork "$BRANCH_NAME"

  # Set the UGent repo as the default remote
  gh repo set-default $REPO_URL

  # Create a pull request using GitHub CLI. Pull request is automatically created into the default repository.
  # Make PR if add + del + mod > 0
  if [ $((N_ADDED_MODULES + N_REMOVED_MODULES + N_MODIFIED_MODULES)) -gt 0 ]; then
    gh pr create \
      --title "$PR_TITLE" \
      --body  "$(make_pr_body "$N_ADDED_MODULES" "$N_REMOVED_MODULES" "$N_MODIFIED_MODULES")" \
      --base  "$BASE_BRANCH" \
      --head  "$fork_user:$BRANCH_NAME"
  else
    echo_info "No changes detected. Skipping PR creation."
  fi


  # Clean up
  rm -rf "$REPO_PATH"
}

main "${1:-}" "${2:-}"