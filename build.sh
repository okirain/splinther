#!/bin/bash
# Build script for Splinther Nuclear Reactor Calculator

set -e  # Exit on error

echo "=================================="
echo "Splinther Build Script"
echo "=================================="
echo ""

# Check for Rust
if ! command -v cargo &> /dev/null; then
    echo "Error: Rust/Cargo not found. Please install Rust from https://rustup.rs/"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

echo "Step 1: Building Rust library..."
echo "----------------------------------"
cargo build --release
echo "✓ Rust library built successfully"
echo ""

echo "Step 2: Running Rust tests..."
echo "----------------------------------"
cargo test
echo "✓ Rust tests passed"
echo ""

echo "Step 3: Installing Python dependencies..."
echo "----------------------------------"
pip install -q pyyaml
echo "✓ Python dependencies installed"
echo ""

echo "Step 4: Running Python tests..."
echo "----------------------------------"
python3 python/tests/test_config.py
echo "✓ Python tests passed"
echo ""

echo "=================================="
echo "Build completed successfully!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. To install the Python module with Rust bindings:"
echo "     $ pip install maturin"
echo "     $ maturin develop --release"
echo ""
echo "  2. To run examples:"
echo "     $ python3 examples/basic_usage.py"
echo "     $ python3 examples/full_integration.py  # (requires maturin build)"
echo ""
