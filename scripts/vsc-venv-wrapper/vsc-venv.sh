SCRIPT_NAME=${BASH_SOURCE[0]} # $0 cannot be used as it gives '-bash' when sourced

usage() {
  echo "Usage: source $SCRIPT_NAME {activate <requirements.txt> [modules.sh] | deactivate}"
  echo ""
  echo "Commands:"
  echo "  activate <requirements_file> [modules_script] Activate the environment using the specified requirements file."
  echo "                                                Optionally, load modules from the specified script before activating the environment."
  echo ""
  echo "  deactivate                                    Deactivate the virtual environment."
  echo ""
  echo "Example Usage:"
  echo "  $ source $SCRIPT_NAME activate requirements.txt modules.sh"
  echo "  $ python my_script.py"
  echo "  $ source $SCRIPT_NAME deactivate"
  return 1
}

echo_info() { echo -e "\e[32m[INFO] $1\e[0m"; }
echo_warning() { echo -e "\e[33m[WARNING] $1\e[0m"; }
echo_error() { echo -e "\e[31m[ERROR] $1\e[0m"; }


# ============================ Main functions ============================

activate() {
  REQUIREMENTS_FILE="$1"
  MODULES_SCRIPT="$2"

  VENV_LOCATION=$(realpath -m "venvs/venv-${VSC_OS_LOCAL}-${VSC_ARCH_LOCAL}") # full path of venv

  # === Step 0: Warn user if they have modules loaded === #

  N_LOADED_MODULES=$(echo "$LOADEDMODULES" | tr ':' '\n' | wc -l)
  if [ "$N_LOADED_MODULES" -gt 4 ]; then # 4 is the number of modules loaded by default
    echo_warning "You have loaded modules in the current shell. If you want to use these modules, please provide a modules script as the second argument."
  fi


  # === Step 1: Purge Modules === #

  echo_info "Purging currently loaded modules."
  module purge

  # === Step 2: Load Modules if module script present === #

  if [ -n "$MODULES_SCRIPT" ]; then # If module script not empty

    echo_info "Loading modules from '$MODULES_SCRIPT'"

    if ! source "$MODULES_SCRIPT"; then # If the module script could not be loaded
        echo_error "Could not load modules from '$MODULES_SCRIPT'"
        return 1
    fi

    echo_info "Modules loaded successfully"

  else
    echo_info "No module script provided. Proceeding without extra modules."
  fi

  # === Step 3: Create Virtual Environment if not yet present === #

  echo_info "Creating virtual environment at $VENV_LOCATION"
  # Will automatically make the venvs folder and venv, does nothing if they already exist
  if ! python -m venv "$VENV_LOCATION"; then
    echo_error "Could not create virtual environment"
    return 1
  fi

  # === Step 4: Activate Virtual Environment === #

  echo_info "Activating virtual environment"
  source "$VENV_LOCATION/bin/activate"

  # === Step 5: Install Requirements === #

  echo_info "Installing requirements from '$REQUIREMENTS_FILE'"
  if ! pip install -r "$REQUIREMENTS_FILE"; then # This will finish quickly if the requirements are already installed
    echo_error "Could not install requirements"
    return 1
  fi
}

deactivate_() {
  echo_info "Deactivating..."
  deactivate # For now, just use the python `deactivate`
}

# ============================ Main ============================

case "$1" in
  activate)    activate "$2" "$3";;
  deactivate)  deactivate_ ;;
  *)           usage ;;
esac