#!/bin/bash

# A script to set up the development environment by managing conda and venv.
#
# This script will:
# 1. Deactivate any currently active conda environment.
# 2. Activate the specified conda environment ('py311').
# 3. Check for a local Python virtual environment (.venv).
# 4. If the .venv does not exist, it will be created using the python from the 'py311' conda env.
# 5. Finally, it will activate the .venv.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# The target conda environment to use for creating the venv.
TARGET_CONDA_ENV="py311"
# The name of the Python virtual environment.
VENV_NAME=".venv"
# --- End Configuration ---


echo "🚀 Starting environment setup..."
echo "---------------------------------"

# Find Conda base directory
# This is more robust than hardcoding the path.
CONDA_BASE_DIR=$(conda info --base)
if [ -z "$CONDA_BASE_DIR" ]; then
    echo "❌ Conda installation not found. Please ensure conda is installed and accessible."
    exit 1
fi

# Source the conda.sh script to make 'conda' command available in the script
source "$CONDA_BASE_DIR/etc/profile.d/conda.sh"
echo "✅ Conda sourced from: $CONDA_BASE_DIR"


# 1. Deactivate any active conda environment
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo "🔵 Deactivating current conda environment: '$CONDA_DEFAULT_ENV'"
    conda deactivate
else
    echo "⚪ No active conda environment to deactivate."
fi

# 2. Activate the target conda environment
echo "🔵 Activating conda environment: '$TARGET_CONDA_ENV'"
conda activate "$TARGET_CONDA_ENV"
echo "✅ Conda environment '$TARGET_CONDA_ENV' is active."
echo "🐍 Using Python from Conda:"
which python


# 3. Check for Python venv and create if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo "🔵 Python venv '$VENV_NAME' not found. Creating it..."
    # Use the python from the activated conda env to create the local venv
    python -m venv "$VENV_NAME"
    echo "✅ Python venv '$VENV_NAME' created."
else
    echo "⚪ Python venv '$VENV_NAME' already exists."
fi

# 4. Activate the Python venv
echo "🔵 Activating Python venv: '$VENV_NAME'"
source "$VENV_NAME/bin/activate"
echo "✅ Python venv '$VENV_NAME' is now active."
echo "🐍 Now using Python from venv:"
which python

# API Keys
echo "Setting up API keys..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not found in environment"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key'"
fi

if [ -z "$TAVILY_API_KEY" ]; then
    echo "⚠️  TAVILY_API_KEY not found in environment"
    echo "Please set it with: export TAVILY_API_KEY='your-tavily-api-key'"
    echo "Get your free API key at: https://tavily.com/"
fi

echo "---------------------------------"
echo "🎉 Environment setup complete!"
echo "You are now in the '$VENV_NAME' virtual environment, which was set up using python from the '$TARGET_CONDA_ENV' conda environment." 