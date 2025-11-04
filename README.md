# Splinther

**Nuclear Reactor Fluid Dynamics Calculator for Space Exploration**

Splinther is a high-performance computational tool for analyzing nuclear reactor fluid dynamics in space applications. It combines the computational power of Rust with the flexibility of Python configuration management.

## Features

- **High-Performance Rust Core**: Fast, accurate fluid dynamics calculations
  - Thermal hydraulics analysis
  - Reynolds number and flow regime determination
  - Heat transfer coefficient calculations
  - Pressure drop analysis
  - Maximum fuel temperature predictions

- **Python Configuration System**: Easy-to-use configuration management
  - YAML and JSON configuration file support
  - Parameter validation with safety limits
  - Export utilities for results

- **Space-Optimized**: Designed for space nuclear reactor applications
  - Liquid sodium coolant properties
  - Compact reactor geometries
  - Microgravity considerations ready

## Architecture

```
┌─────────────────────────────────────┐
│   Python Configuration Layer        │
│  - Config loading (YAML/JSON)       │
│  - Parameter validation             │
│  - Results formatting               │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Rust Computation Engine           │
│  - Thermal hydraulics               │
│  - Fluid dynamics                   │
│  - Heat transfer                    │
│  - Pressure calculations            │
└─────────────────────────────────────┘
```

## Installation

### Prerequisites

- Rust (1.70 or later)
- Python (3.8 or later)
- pip and maturin

### Building the Rust Library

```bash
# Clone the repository
git clone https://github.com/okirain/splinther.git
cd splinther

# Build the Rust library
cargo build --release

# Run Rust tests
cargo test
```

### Installing the Python Package

```bash
# Install Python dependencies
pip install -r requirements.txt

# Build and install the Python module
pip install maturin
maturin develop --release
```

## Usage

### Using Python Configuration System

```python
from splinther_config import ConfigLoader, ConfigValidator

# Load configuration from YAML
config = ConfigLoader.load("configs/small_reactor.yaml")

# Validate configuration
is_valid, messages = ConfigValidator.validate(config)
if not is_valid:
    print("Configuration errors:", messages)
```

### Using the Rust Calculator (via Python)

```python
from splinther import ReactorConfig, ReactorCalculator

# Create configuration
config = ReactorConfig(
    coolant_inlet_temp=600.0,   # Kelvin
    coolant_flow_rate=10.0,     # kg/s
    reactor_power=1e6,          # Watts
    core_height=2.0,            # meters
    core_diameter=0.5,          # meters
    pressure=1e7                # Pascals
)

# Create calculator and run analysis
calculator = ReactorCalculator(config)
results = calculator.calculate()

# Access results
print(f"Outlet Temperature: {results.outlet_temperature:.2f} K")
print(f"Pressure Drop: {results.pressure_drop:.2f} Pa")
print(f"Reynolds Number: {results.reynolds_number:.2e}")
print(f"Heat Transfer Coefficient: {results.heat_transfer_coefficient:.2f} W/m²K")
print(f"Max Fuel Temperature: {results.max_fuel_temperature:.2f} K")
```

### Example Configuration Files

**YAML format** (`configs/small_reactor.yaml`):
```yaml
name: "Small Space Reactor"
description: "Compact nuclear reactor for planetary missions"
coolant_inlet_temp: 600.0
coolant_flow_rate: 5.0
reactor_power: 500000.0
core_height: 1.5
core_diameter: 0.4
pressure: 5000000.0
```

**JSON format** (`configs/example_reactor.json`):
```json
{
  "name": "Example Reactor",
  "coolant_inlet_temp": 650.0,
  "coolant_flow_rate": 10.0,
  "reactor_power": 1000000.0,
  "core_height": 2.0,
  "core_diameter": 0.5,
  "pressure": 7500000.0
}
```

### Running Examples

```bash
# Run basic configuration example
python examples/basic_usage.py
```

## Configuration Parameters

| Parameter | Unit | Description |
|-----------|------|-------------|
| `coolant_inlet_temp` | Kelvin | Coolant inlet temperature |
| `coolant_flow_rate` | kg/s | Mass flow rate of coolant |
| `reactor_power` | Watts | Thermal power output |
| `core_height` | meters | Height of reactor core |
| `core_diameter` | meters | Diameter of reactor core |
| `pressure` | Pascals | System operating pressure |

## Physics Models

### Thermal Hydraulics
- Energy balance calculations
- Coolant outlet temperature
- Maximum fuel temperature estimation
- Uses liquid sodium properties (Cp = 1270 J/kg·K)

### Fluid Dynamics
- Reynolds number calculation
- Flow regime determination (laminar/turbulent)
- Friction factor using Blasius correlation
- Sodium density and viscosity correlations

### Heat Transfer
- Nusselt number (Dittus-Boelter correlation for turbulent flow)
- Heat transfer coefficient
- Thermal conductivity of liquid sodium
- Prandtl number calculations

### Pressure Drop
- Darcy-Weisbach equation
- Friction losses
- Elevation effects
- Pump power requirements

## Testing

### Rust Tests
```bash
cargo test
```

### Python Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest python/tests/
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
│       ├── __init__.py
│       ├── config_loader.py
│       ├── validator.py
│       └── export.py
├── examples/              # Usage examples
│   └── basic_usage.py
├── configs/               # Example configurations
│   ├── small_reactor.yaml
│   ├── large_reactor.yaml
│   └── example_reactor.json
├── Cargo.toml            # Rust dependencies
├── pyproject.toml        # Python package configuration
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use Splinther in your research, please cite:

```
Splinther: Nuclear Reactor Fluid Dynamics Calculator for Space Exploration
https://github.com/okirain/splinther
```

## Acknowledgments

- Liquid sodium property correlations from nuclear engineering literature
- Space reactor design principles from NASA and DOE research
