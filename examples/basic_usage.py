#!/usr/bin/env python3
"""
Basic usage example for Splinther Nuclear Reactor Calculator
Demonstrates configuration loading and validation
"""

import sys
from pathlib import Path

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from splinther_config import ConfigLoader, ConfigValidator, export_to_json
from splinther_config.export import format_results


def main():
    print("Splinther Nuclear Reactor Fluid Dynamics Calculator")
    print("=" * 60)
    print()
    
    # Load configuration from YAML
    config_path = Path(__file__).parent.parent / "configs" / "small_reactor.yaml"
    print(f"Loading configuration from: {config_path}")
    config = ConfigLoader.load_yaml(str(config_path))
    
    print(f"\nReactor: {config.name}")
    print(f"Description: {config.description}")
    print(f"\nConfiguration Parameters:")
    print(f"  Inlet Temperature: {config.coolant_inlet_temp:.2f} K ({config.coolant_inlet_temp - 273.15:.2f} °C)")
    print(f"  Flow Rate: {config.coolant_flow_rate:.2f} kg/s")
    print(f"  Power: {config.reactor_power/1e6:.2f} MW")
    print(f"  Core Height: {config.core_height:.2f} m")
    print(f"  Core Diameter: {config.core_diameter:.2f} m")
    print(f"  Pressure: {config.pressure/1e5:.2f} bar")
    
    # Validate configuration
    print("\n" + "-" * 60)
    print("Validating configuration...")
    is_valid, messages = ConfigValidator.validate(config)
    
    if is_valid:
        print("✓ Configuration is valid")
        if messages:
            print("\nWarnings:")
            for msg in messages:
                print(f"  ⚠ {msg}")
    else:
        print("✗ Configuration validation failed:")
        for msg in messages:
            print(f"  ✗ {msg}")
        return 1
    
    # Note: Actual calculation would require the Rust library to be compiled
    # and installed as a Python module via maturin
    print("\n" + "-" * 60)
    print("\nNote: To perform fluid dynamics calculations, build and install")
    print("the Rust library using maturin:")
    print("  $ cd /path/to/splinther")
    print("  $ pip install maturin")
    print("  $ maturin develop")
    print("\nThen you can use:")
    print("  from splinther import ReactorConfig, ReactorCalculator")
    print("  calculator = ReactorCalculator(config)")
    print("  results = calculator.calculate()")
    
    # Example of what results would look like
    print("\n" + "=" * 60)
    print("\nExample output (simulated):")
    example_results = {
        "outlet_temperature": 718.7,
        "pressure_drop": 15420.5,
        "reynolds_number": 48532.3,
        "heat_transfer_coefficient": 8745.2,
        "max_fuel_temperature": 892.1,
    }
    print(format_results(example_results))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
