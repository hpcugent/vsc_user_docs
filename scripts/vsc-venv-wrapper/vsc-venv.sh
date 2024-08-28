SCRIPT_NAME=${BASH_SOURCE[0]} # $0 cannot be used as it gives '-bash' when sourced

usage() {
  echo "Usage: source $SCRIPT_NAME {activate <requirements.txt> [modules.sh] | deactivate}"
  echo ""
  echo "Commands:"
  echo "  activate <requirements_file> [modules_file] Activate the environment using the specified requirements file."
  echo "                                              Optionally, provide a text file with a list of modules to load."
  echo ""
  echo "  deactivate                                  Deactivate the virtual environment."
  echo ""
  echo "Example Usage:"
  echo "  $ source $SCRIPT_NAME activate requirements.txt modules.txt"
  echo "  $ python my_script.py"
  echo "  $ source $SCRIPT_NAME deactivate"
  return 1
}

echo_info() { echo -e "\e[32m[INFO] $1\e[0m"; }
echo_warning() { echo -e "\e[33m[WARNING] $1\e[0m"; }
echo_error() { echo -e "\e[31m[ERROR] $1\e[0m"; }

load_modules() {
  local modules_file lines
  modules_file="$1"

  if ! mapfile -t lines < "$modules_file"; then # Read the file line by line into an array
    echo_error "Could not read modules script '$modules_file'"
    return 1
  fi

  for line in "${lines[@]}"; do # Loop over each line in the array

    # Skip empty lines
    if [[ -z "$line" ]]; then
      continue
    fi

    if module load "$line"; then
      echo_info "  ✔ Module '$line' loaded successfully"
    else
      echo_error "Could not load module '$line'"
      return 1
    fi

  done

}


# ============================ Main functions ============================

activate() {
  local requirements_file modules_file
  local venv_location n_loaded_modules python_version

  requirements_file="$1"
  modules_file="$2"

  venv_location=$(realpath -m "venvs/venv-${VSC_OS_LOCAL}-${VSC_ARCH_LOCAL}") # full path of venv

  # === Step 0: Warn user if they have modules loaded === #

  loaded_modules=($(echo "$LOADEDMODULES" | tr ':' '\n' | grep -v -E '^(env|cluster)/')) # Remove env and cluster modules
  n_loaded_modules="${#loaded_modules[@]}"
  if [ "$n_loaded_modules" -gt 0 ]; then
    echo_warning "You have $n_loaded_modules loaded modules in the current shell. These modules will be purged."
    echo_warning "If you want to use these modules, please provide a modules file listing the required modules as the second argument."

    echo_warning "Loaded modules:"
    for module in "${loaded_modules[@]}"; do
      echo_warning "  $module"
    done
  fi


  # === Step 1: Purge Modules === #

  echo_info "Purging currently loaded modules."
  module purge

  # === Step 2: Load Modules if module script present === #

  if [ -n "$modules_file" ]; then # If module script not empty

    echo_info "Loading modules from '$modules_file'"

    if ! load_modules "$modules_file"; then # If the modules could not be loaded
      echo_error "Could not load modules from '$modules_file'"
      return 1
    fi

    echo_info "Modules loaded successfully"

  else
    echo_info "No module file provided. Proceeding without extra modules."
  fi

  # === Step 3: Create Virtual Environment if not yet present === #

  if [ "$(which python)" = "/usr/bin/python" ]; then
    echo_warning "System python used. Consider loading a specific python module through the modules script."
  fi

  python_version=$(python --version)
  echo_info "Using $python_version to create virtual environment at $venv_location"
  # Will automatically make the venvs folder and venv, does nothing if they already exist
  if ! python -m venv "$venv_location"; then
    echo_error "Could not create virtual environment"
    return 1
  fi

  # === Step 4: Activate Virtual Environment === #

  echo_info "Activating virtual environment"
  source "$venv_location/bin/activate"

  # === Step 5: Install Requirements === #

  echo_info "Installing requirements from '$requirements_file'"
  if ! pip install -r "$requirements_file"; then # This will finish quickly if the requirements are already installed
    echo_error "Could not install requirements"
    deactivate
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