# Contributing to Splinther

Thank you for your interest in contributing to Splinther! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Prerequisites

- Rust 1.70 or later
- Python 3.8 or later
- Git

### Setting Up Your Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/okirain/splinther.git
   cd splinther
   ```

2. **Install Rust dependencies**
   ```bash
   cargo build
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   pip install maturin pytest pytest-cov
   ```

4. **Run the build script**
   ```bash
   ./build.sh
   ```

## Project Structure

```
splinther/
├── src/                    # Rust source code
│   ├── lib.rs             # Main library and Python bindings
│   ├── thermal_hydraulics.rs
│   ├── fluid_dynamics.rs
│   ├── heat_transfer.rs
│   └── pressure.rs
├── python/                 # Python configuration system
│   └── splinther_config/
├── examples/              # Usage examples
├── configs/               # Example configurations
└── tests/                 # Test files
```

## Making Changes

### Rust Code

1. **Write tests first** - Add tests to the relevant module's `#[cfg(test)]` section
2. **Follow Rust conventions** - Use `cargo fmt` and `cargo clippy`
3. **Document public APIs** - Add doc comments to public functions and types
4. **Run tests** - Execute `cargo test` before committing

Example:
```rust
/// Calculate outlet temperature of coolant
/// 
/// # Arguments
/// * `inlet_temp` - Inlet temperature in Kelvin
/// * `power` - Reactor thermal power in Watts
/// 
/// # Returns
/// Outlet temperature in Kelvin
pub fn calculate_outlet_temperature(inlet_temp: f64, power: f64) -> f64 {
    // Implementation
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_outlet_temperature() {
        // Test implementation
    }
}
```

### Python Code

1. **Follow PEP 8** - Use `black` or `autopep8` for formatting
2. **Add type hints** - Use Python type annotations
3. **Write docstrings** - Document functions and classes
4. **Write tests** - Add tests to `python/tests/`

Example:
```python
def calculate_something(param: float) -> float:
    """
    Calculate something based on parameter
    
    Args:
        param: Input parameter
        
    Returns:
        Calculated result
    """
    return param * 2.0
```

## Testing

### Running Tests

**Rust tests:**
```bash
cargo test
```

**Python tests:**
```bash
python3 -m pytest python/tests/
# or
python3 python/tests/test_config.py
```

**All tests:**
```bash
./build.sh
```

### Writing Tests

- Add unit tests for all new functions
- Test edge cases and error conditions
- Ensure tests are deterministic and fast
- Use meaningful test names that describe what is being tested

## Code Review Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run all tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include test coverage for new code
- Ensure all tests pass
- Update documentation as needed
- Keep PRs focused on a single feature or fix

## Coding Standards

### Rust

- Use `cargo fmt` for formatting
- Run `cargo clippy` and address warnings
- Follow Rust API guidelines
- Use meaningful variable and function names
- Keep functions focused and small
- Avoid unwrap() in library code - use Result/Option

### Python

- Follow PEP 8 style guide
- Use type hints for function signatures
- Keep functions under 50 lines when possible
- Use meaningful variable names
- Document complex logic with comments

## Documentation

- Update README.md if you change user-facing features
- Add doc comments to all public APIs
- Include usage examples for new features
- Update configuration examples if parameters change

## Physics and Engineering

When contributing physics calculations:

1. **Cite sources** - Reference papers, textbooks, or standards
2. **Document assumptions** - Clearly state any simplifying assumptions
3. **Include units** - Always specify units in comments and documentation
4. **Validate results** - Compare with known solutions or benchmarks
5. **Consider edge cases** - Think about physical limits and constraints

Example:
```rust
/// Calculate Reynolds number for flow characterization
/// 
/// Uses the definition: Re = ρ * V * D / μ
/// 
/// Reference: White, F.M. (2011). Fluid Mechanics, 7th ed.
/// 
/// # Arguments
/// * `velocity` - Flow velocity in m/s
/// * `diameter` - Characteristic length in meters
/// 
/// # Returns
/// Reynolds number (dimensionless)
```

## Getting Help

- Open an issue for bugs or feature requests
- Discuss major changes in an issue before starting work
- Ask questions in pull request comments

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- Git commit history

Thank you for contributing to Splinther!
