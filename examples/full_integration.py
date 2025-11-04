#!/usr/bin/env python3
"""
Full integration example for Splinther
Demonstrates the complete workflow from configuration to calculation

Note: This example requires the Rust library to be built and installed:
    $ pip install maturin
    $ maturin develop --release
"""

import sys
from pathlib import Path

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from splinther_config import ConfigLoader, ConfigValidator
from splinther_config.export import format_results


def run_calculation_example():
    """
    Example showing how to use the Rust calculator
    (Requires maturin build and installation)
    """
    try:
        # Try to import the Rust module
        from splinther import ReactorConfig, ReactorCalculator
        
        print("Splinther Full Integration Example")
        print("=" * 70)
        print()
        
        # Load configuration from file
        config_path = Path(__file__).parent.parent / "configs" / "large_reactor.yaml"
        print(f"Loading configuration: {config_path.name}")
        py_config = ConfigLoader.load(str(config_path))
        
        print(f"\nReactor: {py_config.name}")
        print(f"Description: {py_config.description}")
        print(f"\nConfiguration:")
        print(f"  Power: {py_config.reactor_power/1e6:.2f} MW")
        print(f"  Inlet Temp: {py_config.coolant_inlet_temp:.1f} K")
        print(f"  Flow Rate: {py_config.coolant_flow_rate:.1f} kg/s")
        print(f"  Pressure: {py_config.pressure/1e5:.1f} bar")
        
        # Validate configuration
        print("\n" + "-" * 70)
        print("Validating configuration...")
        is_valid, messages = ConfigValidator.validate(py_config)
        
        if not is_valid:
            print("✗ Configuration validation failed:")
            for msg in messages:
                print(f"  ✗ {msg}")
            return 1
        
        print("✓ Configuration is valid")
        if messages:
            print("\nWarnings:")
            for msg in messages:
                print(f"  ⚠ {msg}")
        
        # Create Rust configuration object
        print("\n" + "-" * 70)
        print("Creating calculator...")
        rust_config = ReactorConfig(
            coolant_inlet_temp=py_config.coolant_inlet_temp,
            coolant_flow_rate=py_config.coolant_flow_rate,
            reactor_power=py_config.reactor_power,
            core_height=py_config.core_height,
            core_diameter=py_config.core_diameter,
            pressure=py_config.pressure
        )
        
        calculator = ReactorCalculator(rust_config)
        
        # Perform calculations
        print("Running fluid dynamics analysis...")
        results = calculator.calculate()
        
        # Display results
        print("\n" + "=" * 70)
        print("\nCALCULATION RESULTS")
        print("=" * 70)
        
        print(f"\nCoolant Temperatures:")
        print(f"  Inlet:  {py_config.coolant_inlet_temp:.2f} K ({py_config.coolant_inlet_temp - 273.15:.2f} °C)")
        print(f"  Outlet: {results.outlet_temperature:.2f} K ({results.outlet_temperature - 273.15:.2f} °C)")
        print(f"  Rise:   {results.outlet_temperature - py_config.coolant_inlet_temp:.2f} K")
        
        print(f"\nFuel Temperature:")
        print(f"  Maximum: {results.max_fuel_temperature:.2f} K ({results.max_fuel_temperature - 273.15:.2f} °C)")
        
        print(f"\nFlow Characteristics:")
        print(f"  Reynolds Number: {results.reynolds_number:.2e}")
        flow_regime = "Turbulent" if results.reynolds_number > 4000 else "Laminar"
        print(f"  Flow Regime: {flow_regime}")
        
        print(f"\nHeat Transfer:")
        print(f"  Heat Transfer Coefficient: {results.heat_transfer_coefficient:.2f} W/m²·K")
        
        print(f"\nPressure Analysis:")
        print(f"  Pressure Drop: {results.pressure_drop:.2f} Pa ({results.pressure_drop/1e3:.2f} kPa)")
        print(f"  Inlet Pressure: {py_config.pressure/1e5:.2f} bar")
        print(f"  Outlet Pressure: {(py_config.pressure - results.pressure_drop)/1e5:.2f} bar")
        
        print("\n" + "=" * 70)
        print("\nAnalysis complete!")
        
        return 0
        
    except ImportError as e:
        print("Error: Rust library not installed")
        print("\nTo build and install the Splinther Rust library:")
        print("  $ pip install maturin")
        print("  $ cd /path/to/splinther")
        print("  $ maturin develop --release")
        print(f"\nDetails: {e}")
        return 1


def compare_configurations():
    """
    Compare different reactor configurations
    """
    print("\nConfiguration Comparison")
    print("=" * 70)
    
    configs_dir = Path(__file__).parent.parent / "configs"
    configs = [
        configs_dir / "small_reactor.yaml",
        configs_dir / "large_reactor.yaml",
    ]
    
    print(f"\n{'Parameter':<25} {'Small Reactor':<20} {'Large Reactor':<20}")
    print("-" * 70)
    
    configs_data = []
    for config_path in configs:
        config = ConfigLoader.load(str(config_path))
        configs_data.append(config)
    
    # Compare key parameters
    comparisons = [
        ("Power (MW)", lambda c: f"{c.reactor_power/1e6:.2f}"),
        ("Inlet Temp (K)", lambda c: f"{c.coolant_inlet_temp:.0f}"),
        ("Flow Rate (kg/s)", lambda c: f"{c.coolant_flow_rate:.1f}"),
        ("Core Height (m)", lambda c: f"{c.core_height:.2f}"),
        ("Core Diameter (m)", lambda c: f"{c.core_diameter:.2f}"),
        ("Pressure (bar)", lambda c: f"{c.pressure/1e5:.1f}"),
    ]
    
    for param_name, formatter in comparisons:
        values = [formatter(c) for c in configs_data]
        print(f"{param_name:<25} {values[0]:<20} {values[1]:<20}")


if __name__ == "__main__":
    # Try to run full integration with Rust
    result = run_calculation_example()
    
    if result != 0:
        print("\n" + "=" * 70)
        print("\nFalling back to configuration comparison only...")
        compare_configurations()
    
    sys.exit(result)
