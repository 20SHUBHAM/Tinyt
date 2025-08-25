#!/bin/bash

# Deployment script for Replit
echo "🚀 Deploying Agentic Focus Group Platform to Replit..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data cache logs

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy environment template if .env doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys!"
fi

# Run setup test
echo "🧪 Running setup test..."
python test_setup.py

# Check if test passed
if [ $? -eq 0 ]; then
    echo "✅ Setup test passed!"
    echo ""
    echo "🎉 Deployment complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your API keys"
    echo "2. Click 'Run' button in Replit"
    echo "3. Access your app via the generated URL"
    echo ""
    echo "📚 Check README.md for detailed instructions"
else
    echo "❌ Setup test failed. Please check the errors above."
    exit 1
fi