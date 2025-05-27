#!/bin/bash

echo "Setting up Django Multi-Step Profile Form..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Populate sample data
echo "Populating sample location data..."
python manage.py populate_locations

# Create static directory
echo "Creating static directory..."
mkdir -p static/css

echo "Setup complete! Run 'python manage.py runserver' to start the development server."
