#!/usr/bin/env bash
# Render build script for AI Voice Detection API

set -o errexit  # Exit on error

echo "===== Upgrading pip and build tools ====="
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel

echo "===== Installing Python dependencies ====="
pip install -r requirements.txt

echo "===== Build completed successfully ====="

