#!/bin/bash

echo "🚀 Setting up Google Login App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed. Please install Node.js and try again."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd client
npm install
cd ..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd server
pip install -r requirements.txt
cd ..

# Copy environment file
echo "📝 Setting up environment file..."
if [ ! -f "server/.env" ]; then
    cp server/env.example server/.env
    echo "⚠️  Please edit server/.env with your Google OAuth credentials"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit server/.env with your Google OAuth credentials"
echo "2. Run 'npm run dev' to start the development servers"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "For Google OAuth setup instructions, see README.md" 