#!/usr/bin/env zsh
set -euo pipefail

# ==========================================================
# setup-python-env.zsh
# ----------------------------------------------------------
#
# Create a Python development environment using:
#   - uv (fast Python package/project manager)
#   - direnv (.envrc auto-activation)
#
# Two modes:
#   Default: installs full dev environment (LSP, typing, tests, docs)
#   --minimal: installs only python-lsp-server[all] and ruff
#
# Usage:
#   setup-python-env.zsh [OPTIONS] <PROJECT_NAME>
#
# Options:
#   -p, --python <version>   Specify Python version (default: latest available)
#   --minimal                Install only essential LSP and lint tools
#   -h, --help               Show this help message and exit
#
# Examples:
#   setup-python-env.zsh my-project
#   setup-python-env.zsh --minimal my-project
#   setup-python-env.zsh -p 3.12 my-project
#
# Requirements:
#   - zsh
#   - uv
#   - direnv
#
# ==========================================================

PYTHON_VERSION=""
PROJECT_NAME=""
MINIMAL_MODE=false

# Full development environment
LSP_PACKAGES_FULL=(
    "python-lsp-server[all]"
    pylsp-mypy
    mypy
    python-dotenv
    ruff
    pytest
    pytest-cov
    sphinx
    ipython
)

# Minimal environment
LSP_PACKAGES_MINIMAL=(
    "python-lsp-server[all]"
    ruff
)

show_help() {
    sed -n '7,33p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
    -p | --python)
        PYTHON_VERSION="$2"
        shift 2
        ;;
    --minimal)
        MINIMAL_MODE=true
        shift
        ;;
    -h | --help)
        show_help
        ;;
    -*)
        echo "Unknown option: $1" >&2
        echo "Use --help for usage." >&2
        exit 1
        ;;
    *)
        PROJECT_NAME="$1"
        shift
        ;;
    esac
done

if [[ -z "$PROJECT_NAME" ]]; then
    echo "Error: project name is required." >&2
    echo "Usage: $0 [OPTIONS] <project-name>" >&2
    exit 1
fi

echo "Creating Python environment for: $PROJECT_NAME"

mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize uv project
if [[ -n "$PYTHON_VERSION" ]]; then
    echo "Using Python version: $PYTHON_VERSION"
    uv init --python "$PYTHON_VERSION"
else
    echo "Using latest available Python version..."
    uv init
fi

# Auto-activation via direnv
cat >.envrc <<'EOF'
# Automatically activate uv environment
layout uv
EOF

direnv allow

# Choose package set
if $MINIMAL_MODE; then
    LSP_PACKAGES=("${LSP_PACKAGES_MINIMAL[@]}")
    echo "Installing minimal development packages..."
else
    LSP_PACKAGES=("${LSP_PACKAGES_FULL[@]}")
    echo "Installing full development package set..."
fi

uv add --dev "${LSP_PACKAGES[@]}"

# Editor configuration
cat >.editorconfig <<'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space

[*.py]
indent_size = 4
max_line_length = 79

[*.{yml,yaml,json,toml,sh}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab

[*.rst]
max_line_length = off

EOF

echo "Setup complete."
echo "Project: $PROJECT_NAME"
echo "Python version: ${PYTHON_VERSION:-latest available}"
echo "Environment: uv + direnv"
echo "Installed dev packages:"
for pkg in "${LSP_PACKAGES[@]}"; do
    echo "  - $pkg"
done
