#!/bin/bash
# Quick setup script for strands-spot

echo "🦆 Setting up strands-spot..."
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set environment variables:"
echo "   export SPOT_HOSTNAME=\"192.168.80.3\""
echo "   export SPOT_USERNAME=\"admin\""
echo "   export SPOT_PASSWORD=\"password\""
echo ""
echo "2. Test connection:"
echo "   python examples/test_connection.py"
echo ""
echo "3. Run examples:"
echo "   python examples/basic_control.py"
echo "   python examples/image_capture.py"
echo "   python examples/velocity_control.py"
