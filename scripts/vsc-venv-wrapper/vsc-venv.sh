#!/usr/bin/env bash

VENV_NAME="venv-${VSC_OS_LOCAL}-${VSC_ARCH_LOCAL}"
VENV_LOCATION=$(realpath -m "venvs/$VENV_NAME") # full path of venv

usage() {
  echo "Usage: $0 {create <optional: modules>|install <requirements>|activate}"
  echo ""
  echo "Commands:"
  echo "  create [modules_script]  Create a virtual environment at $VENV_LOCATION."
  echo "                           Optionally, load modules from the specified script before creating the environment."
  echo "  install <requirements>   Install packages from the specified requirements file."
  echo "                           The virtual environment must be activated before running this command."
  echo "  activate                 Activate the virtual environment. You need to source this command."
  echo ""
  echo "Example Usage:"
  echo "  $ $0 create my_modules.sh"
  echo "  $ source $0 activate"
  echo "  $ $0 install requirements.txt"
  echo "  $ python my_script.py"
  echo "  $ deactivate"
  exit 1
}

# ============================ Main functions ============================

# === Create ===

create() {
  local MODULES_SCRIPT="$1" # The modules script to load. Empty if not provided.

  echo "INFO: Creating virtual environment with modules $MODULES_SCRIPT..."

  # If a modules script is provided, try to load it.
  if [ -n "$MODULES_SCRIPT" ]; then
    echo "INFO: loading modules from '$MODULES_SCRIPT'"

    # If the module script could not be loaded, exit.
    if ! source "$MODULES_SCRIPT"; then
        echo "ERROR: could not load modules from '$MODULES_SCRIPT'"
        exit 1
    fi
  fi

  # Create a virtual environment
  echo "INFO: creating virtual environment at $VENV_LOCATION"
  if ! python -m venv "$VENV_LOCATION"; then
    echo "ERROR: could not create virtual environment"
    exit 1
  fi


}

# === Activate ===

activate() {
  echo "Activating..."

  # If the virtual environment does not exist, exit.
  if [ ! -f "$VENV_LOCATION/bin/activate" ]; then
    echo "ERROR: virtual environment does not exist. Run 'create' first."
    exit 1
  fi

  source "$VENV_LOCATION/bin/activate"
}

# === Install ===

install() {

  local REQUIREMENTS="$1"
  echo "Installing $REQUIREMENTS..."

  # If no requirements file is provided, exit.
  if [ ! -f "$REQUIREMENTS" ]; then
    echo "ERROR: no requirements file provided"
    exit 1
  fi

  # The virtual environment must have been activated before running install.
  # This is equivalent to $VIRTUAL_ENV (which is set by python when activating a venv) being equal to
  # $VENV_LOCATION (the location of the venv specific to the architecture of the target cluster).
  if [ "$VIRTUAL_ENV" != "$VENV_LOCATION" ]; then
        echo "ERROR: virtual environment is not activated. Run 'activate' first."
        exit 1
  fi

  # Install the requirements
  if ! pip install -r "$REQUIREMENTS"; then
    echo "ERROR: could not install requirements"
    exit 1
  fi

}

# ============================ Main ============================

case "$1" in
  create)     create "$2";;
  install)    install "$2" ;;
  activate)   activate ;;
  *)          usage ;;
esac
