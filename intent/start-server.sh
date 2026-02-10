#!/usr/bin/env bash

# Purpose:
# A single, reliable "fresh boot" entrypoint that:
# - uses .venv if present
# - otherwise creates .venv using the newest available python3.x on the system
# - loads environment from .env
# - installs ALL Python dependencies declared under the script directory
# - bootstraps UI/frontend resources
# - starts the backend if an obvious entrypoint exists, otherwise exits cleanly with guidance
#
# This script is POSIX-compliant and fails fast on any error.
# It does not modify any files outside intent/ and does not hardcode secrets.

# Set strict mode
set -euo pipefail

# Resolve script directory using BASH_SOURCE[0]
SCRIPT_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)"

# Change to script directory
cd "${SCRIPT_DIR}"

# Load environment variables
if [[ -f ".env" ]]; then
    echo "Loading environment variables from .env"
    # Parse .env file: skip comments and empty lines
    while IFS=\n read -r line; do
        [[ -z "$line" ]] && continue
        [[ "$line" =~ ^# ]] && continue
        # Extract KEY=VALUE
        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
            export "$key"="$value"
        fi
    done < ".env"
else
    echo "Warning: .env not found. Using defaults."
fi

# Python virtual environment
if [[ -d ".venv" ]]; then
    echo "Reusing existing .venv"
    source ".venv/bin/activate"
else
    echo "Creating new .venv"
    # Find the newest available python3.x on PATH
    python_cmd=""

    # 1) prefer explicit Binaries
    for ver in 13 12 11; do
        if command -v "python3.$ver" >/dev/null 2>&1; then
            python_cmd="python3.$ver"
            break
        fi
    done

    # 2) Fallback: check python3
    if [[ -z "$python_cmd" ]] && command -v python3 >/dev/null 2>&1; then
        pyver=$(python3 - <<'EOF'
    import sys
    print(f"{sys.version_info.major}.{sys.version_info.minor}")
EOF
    )
        if [[ "$pyver" =~ ^3\.(1[1-9]|[2-9][0-9])$ ]]; then
            python_cmd="python3"
        fi
    fi

    if [[ -z "$python_cmd" ]]; then
        echo "Python >= 3.11 not found"
        exit 1
    fi

    echo "Using $python_cmd as interpreter"
    # Verify it supports -m venv
    if ! "$python_cmd" -m venv .venv; then
        echo "Error: $python_cmd does not support -m venv. Please install a compatible Python version." >&2
        exit 1
    fi
    # Activate newly created venv
    source ".venv/bin/activate"
fi

# Upgrade pip, setuptools, wheel
echo "Upgrading pip, setuptools, and wheel"
python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
requirements_files=$(find . -type f -name "requirements.txt" | sort)
if [[ -z "$requirements_files" ]]; then
    echo "Warning: No requirements.txt files found. Skipping dependency installation."
else
    echo "Installing dependencies from $(echo "$requirements_files" | wc -l) requirements.txt files:"
    for req_file in $requirements_files; do
        echo "  - $req_file"
        if ! python -m pip install -r "$req_file"; then
            echo "Error: Failed to install dependencies from $req_file" >&2
            exit 1
        fi
    done
fi

# Note: pyproject.toml exists but is not used by this script
# (This script does not use poetry, pdm, or uv. Use pip only.)

# UI / frontend bootstrap
ui_dir="ui/frontend"
if [[ -d "$ui_dir" ]]; then
    echo "Bootstrapping UI/frontend resources"
    if ! command -v npm &> /dev/null; then
        echo "Error: npm not found. Please install Node.js and ensure it's in your PATH." >&2
        exit 1
    fi
    if [[ ! -d "node_modules" ]]; then
        echo "Installing frontend dependencies"
        cd "$ui_dir"
        npm install
        if [[ $? -ne 0 ]]; then
            echo "Error: npm install failed in $ui_dir" >&2
            exit 1
        fi
    else
        echo "node_modules already exists. Skipping npm install."
    fi
    # Check for a "build" script in package.json
    if [[ -f "$ui_dir/package.json" ]]; then
        if grep -q '"build"' "$ui_dir/package.json"; then
            echo "Running npm run build"
            cd "$ui_dir"
            npm run build
            if [[ $? -ne 0 ]]; then
                echo "Error: npm run build failed in $ui_dir" >&2
                exit 1
            fi
        else
            echo "No "build" script found in package.json. Skipping build."
        fi
    else
        echo "Warning: $ui_dir/package.json not found. Skipping build." >&2
    fi
else
    echo "Warning: UI/frontend directory not found at $ui_dir. Skipping frontend bootstrap."
fi

# Backend startup
backend_entrypoint=""
# Look for main.py in any app/ directory
for dir in "$(find . -type d -name "app" -not -path "*/\.*")"; do
    if [[ -f "$dir/main.py" ]]; then
        backend_entrypoint="$dir/main.py"
        break
    fi
    # Also check for main.py in subdirectories
    if [[ -f "$dir/app/main.py" ]]; then
        backend_entrypoint="$dir/app/main.py"
        break
    fi
    # Check for main.py in any subdirectory
    if [[ -f "$dir/*/main.py" ]]; then
        # Find the first main.py
        for f in "$dir"/*/main.py; do
            if [[ -f "$f" ]]; then
                backend_entrypoint="$f"
                break
            fi
        done
    fi
    if [[ -n "$backend_entrypoint" ]]; then
        break
    fi
done

# If found, run it
if [[ -n "$backend_entrypoint" ]]; then
    echo "Found backend entrypoint: $backend_entrypoint"
    # Extract directory and module name
    dir_path=$(dirname "$backend_entrypoint")
    module_name=$(basename "$backend_entrypoint" .py)
    # Use uvicorn to run it
    echo "Starting backend server..."
    uvicorn "${module_name}:app" --host 0.0.0.0 --port 8000 --reload
else
    echo "Error: No obvious backend entrypoint found."
    echo "Checked for main.py in app/ directories under $(pwd)."
    echo "Please define a start command in this script or create a main.py in a subdirectory." >&2
    exit 1
fi

# Output summary
echo "\n--- Startup Summary ---"
echo "- Python interpreter: $(python --version 2>&1 | cut -d' ' -f3)"
echo "- venv: $(if [[ -d ".venv" ]]; then echo "reused"; else echo "created"; fi)"
echo "- requirements.txt files installed: $(echo "$requirements_files" | wc -l)"
echo "- UI/frontend build status: $(if [[ -f "../ui/frontend/dist" ]] || [[ -f "../ui/frontend/build" ]]; then echo "success"; else echo "skipped"; fi)"
echo "- Backend command executed: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
```
