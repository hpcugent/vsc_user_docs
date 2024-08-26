usage() {
  echo "Usage: source $0 {activate <requirements.txt> [modules.sh] | deactivate}"
  echo ""
  echo "Commands:"
  echo "  activate <requirements_file> [modules_script] Activate the environment using the specified requirements file."
  echo "                                                Optionally, load modules from the specified script before activating the environment."
  echo ""
  echo "  deactivate                                    Deactivate the virtual environment."
  echo ""
  echo "Example Usage:"
  echo "  $ source $0 activate requirements.txt modules.sh"
  echo "  $ python my_script.py"
  echo "  $ source $0 deactivate"
  return 1
}

# ============================ Main functions ============================

activate() {
  REQUIREMENTS_FILE="$1"
  MODULES_SCRIPT="$2"

  VENV_LOCATION=$(realpath -m "venvs/venv-${VSC_OS_LOCAL}-${VSC_ARCH_LOCAL}") # full path of venv

  # === Step 0: Warn user if they have modules loaded === #
  N_MODULES_LOADED=$(echo "$LOADEDMODULES" | tr ':' '\n' | wc -l)
  if [ "$N_MODULES_LOADED" -gt 4 ]; then # 4 is the number of modules loaded by default
    echo "WARNING: You have loaded modules in the current shell.
    if you want to use these modules, please provide a modules script as the second argument."
  fi


  # === Step 1: Purge Modules === #
  echo "INFO: Purging currently loaded modules. If you want to use modules, provide a modules script."
  module purge

  # === Step 2: Load Modules if module script present === #

  if [ -n "$MODULES_SCRIPT" ]; then

    echo "INFO: loading modules from '$MODULES_SCRIPT'"

    # If the module script could not be loaded, return.
    if ! source "$MODULES_SCRIPT"; then
        echo "ERROR: could not load modules from '$MODULES_SCRIPT'"
        return 1
    fi

    echo "INFO: Modules loaded successfully"

  else
    echo "INFO: No module script provided. Proceeding without extra modules."
  fi

  # === Step 3: Create Virtual Environment if not yet present === #

  echo "INFO: creating virtual environment at $VENV_LOCATION"
  # Will automatically make the venvs folder and venv, does nothing if they already exist
  if ! python -m venv "$VENV_LOCATION"; then
    echo "ERROR: could not create virtual environment"
    return 1
  fi

  # === Step 4: Activate Virtual Environment === #

  source "$VENV_LOCATION/bin/activate"

  # === Step 5: Install Requirements === #

  echo "INFO: installing requirements from '$REQUIREMENTS_FILE'"
  pip install -r "$REQUIREMENTS_FILE" # This will finish quickly if the requirements are already installed

}

deactivate_() {
  echo "INFO: Deactivating..."
  deactivate # For now, just use the python `deactivate`
}

# ============================ Main ============================

case "$1" in
  activate)     activate "$2" "$3";;
  deactivate)  deactivate_ ;;
  *)            usage ;;
esac