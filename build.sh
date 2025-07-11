#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
VENV_DIR=".venv"
SERVICE_FILE="htmlparser.service"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="htmlparser.service"

echo "Creating Python virtual environment in $VENV_DIR..."
python3 -m venv $VENV_DIR

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Deactivating virtual environment..."
deactivate

echo "Copying $SERVICE_FILE to $SYSTEMD_DIR..."
sudo cp $SERVICE_FILE $SYSTEMD_DIR/

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling $SERVICE_NAME to start on boot..."
sudo systemctl enable $SERVICE_NAME

echo "Starting (or restarting) $SERVICE_NAME service..."
sudo systemctl restart $SERVICE_NAME

echo "Installation and service setup complete."
