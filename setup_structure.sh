#!/bin/bash

# Create framework directory structure
mkdir -p config
mkdir -p pages
mkdir -p tests
mkdir -p utils
mkdir -p reports
mkdir -p screenshots
mkdir -p logs
mkdir -p fixtures

# Create __init__.py files
touch config/__init__.py
touch pages/__init__.py
touch tests/__init__.py
touch utils/__init__.py
touch fixtures/__init__.py

echo "Framework structure created successfully!"
