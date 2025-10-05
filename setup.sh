#!/bin/bash
# Setup script for AI Personal Productivity Assistant
# This script helps users set up their local environment safely

set -e

echo "🤖 AI Personal Productivity Assistant - Setup Script"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION is not supported. Please upgrade to Python $REQUIRED_VERSION or higher."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ~/.ai_productivity_assistant/{data,logs,models,config,backups}

# Copy example configuration
if [ ! -f ~/.ai_productivity_assistant/config/user_config.yaml ]; then
    echo "📋 Setting up configuration..."
    cp config/example_config.yaml ~/.ai_productivity_assistant/config/user_config.yaml
    echo "✅ Created user configuration at ~/.ai_productivity_assistant/config/user_config.yaml"
    echo "⚠️  Please edit this file to customize your privacy settings before running the application."
else
    echo "ℹ️  User configuration already exists"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔐 Setting up environment variables..."
    cat > .env << EOF
# Environment variables for AI Personal Productivity Assistant
# Add any sensitive configuration here (this file is gitignored)

# Database path (already configured in user_config.yaml)
# DATABASE_PATH=~/.ai_productivity_assistant/data.db

# Optional: API keys for future features (if any)
# OPENAI_API_KEY=your_key_here

# Development settings
DEBUG=false
LOG_LEVEL=INFO
EOF
    echo "✅ Created .env file"
else
    echo "ℹ️  .env file already exists"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ pip is not installed. Please install pip and run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies installed"

# Create desktop shortcut (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🖥️  Creating desktop shortcut..."
    cat > ~/Desktop/AI_Productivity_Assistant.command << EOF
#!/bin/bash
cd "$(dirname "$0")"
source .env
python3 src/main.py
EOF
    chmod +x ~/Desktop/AI_Productivity_Assistant.command
    echo "✅ Desktop shortcut created"
fi

# Run basic health check
echo "🔍 Running health check..."
python3 -c "
import sys
print('✅ Python version:', sys.version)
try:
    import pandas as pd
    print('✅ pandas available')
except ImportError:
    print('❌ pandas not available')

try:
    import sklearn
    print('✅ scikit-learn available')
except ImportError:
    print('❌ scikit-learn not available')

try:
    import tensorflow as tf
    print('✅ TensorFlow available')
except ImportError:
    print('❌ TensorFlow not available')

print('✅ Basic health check completed')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit ~/.ai_productivity_assistant/config/user_config.yaml to customize privacy settings"
echo "2. Review and update .env file if needed"
echo "3. Run the application: python3 src/main.py"
echo ""
echo "🔒 Security reminders:"
echo "- Never commit files in ~/.ai_productivity_assistant/ to git"
echo "- Review .gitignore to ensure sensitive files are excluded"
echo "- Keep your user_config.yaml private"
echo ""
echo "📖 For more information, see SECURITY.md and README.md"