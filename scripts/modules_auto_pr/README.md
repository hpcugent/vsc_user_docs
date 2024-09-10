# Auto Update Modules Script

This script automates the process of updating markdown files in the `vsc_user_docs` repository by 

- cloning the `hpcugent/vsc_user_docs` repository
- creating a new branch
- running the `available_software.py` script
- committing the changes
- pushing the changes to a forked repository
- creating a pull request to the `hpcugent/vsc_user_docs` repository from the forked repository using a GitHub Personal Access Token (PAT)

## Assumptions of the script

The script assumes the following:

- The user who owns the fork has a GitHub personal access token (PAT) with the `repo` and `read:org` scopes. This is used to create the pull request.
- SSH keys need to be present for the GitHub account that owns the fork. This will be used to push the changed to the fork. This is different from the PAT, which is only used to create the pull request.
- Lmod is installed. This is used by the `available_software.py` script.
- The GitHub CLI (`gh`) is installed to create the PR. See [the GitHub CLI installation instructions](https://github.com/cli/cli#installation) for more information.
- the fork is named `vsc_user_docs`

## Usage

The script should be called with a file containing a
[GitHub classic personal access token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#personal-access-tokens-classic) 
and the GitHub name of the user which owns the fork as arguments:

```shell
$ ./modules_auto_pr.sh path/to/github/PAT <github_username>
```

## Make a classic Personal Access Token

To make a classic PAT, navigate to the GitHub account setting page (not the repository settings) and go to:

> Developer settings > Personal access tokens > Tokens (classic)

click on `Generate new token` and fill in the note field and expiration date. 

Under `select scopes`, click on `repo` (which will automatically select all the sub-scopes) and `read:org` (which is a sub-scope of `admin:org`).

Click generate token and copy-paste the token into the file that is passed to the `modules_auto_pr.sh` script (see above)

The reason fine-grained tokens are not used is that they do not yet support writing to a public repository 
that is not owned by you or an organization that you are not a member of.



