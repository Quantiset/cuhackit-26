#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting installation for cuhackit-26..."

# Check for Git
if ! [ -x "$(command -v git)" ]; then
  echo 'Error: git is not installed.' >&2
  exit 1
fi

# Clone the repository if the folder doesn't exist
if [ ! -d ".git" ]; then
    echo "Cloning repository..."
    git clone https://github.com/Quantiset/cuhackit-26.git .
fi

# Determine project type and install dependencies
if [ -f "package.json" ]; then
    echo "📦 Node.js project detected. Installing dependencies..."
    npm install
elif [ -f "requirements.txt" ]; then
    echo "🐍 Python project detected. Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Handle environment variables
if [ -f ".env.example" ]; then
    echo "⚙️ Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "✅ Installation complete!"
