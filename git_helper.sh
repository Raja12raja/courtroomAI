#!/bin/bash
# Git Helper Script for Databricks
# This script sets up the environment for git operations

# Set safe directory
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0="safe.directory"
export GIT_CONFIG_VALUE_0="/Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app"

# Change to app directory
cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/

# Execute git command passed as arguments
git "$@"
