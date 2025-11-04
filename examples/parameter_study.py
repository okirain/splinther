#!/usr/bin/env python3
"""
Parameter study example for Splinther
Demonstrates how to analyze reactor performance across different operating conditions

This example performs a parametric study without requiring the Rust library,
showing configuration validation and analysis capabilities.
"""

import sys
from pathlib import Path

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from splinther_config import ReactorConfiguration, ConfigValidator


def analyze_power_sweep():
    """
    Analyze reactor performance at different power levels
    """
    print("Power Level Analysis")
    print("=" * 80)
    print()
    
    base_config = ReactorConfiguration(
        coolant_inlet_temp=600.0,
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7,
        name="Base Configuration"
    )
    
    # Test different power levels
    power_levels = [0.5e6, 1.0e6, 2.0e6, 5.0e6, 10.0e6]  # Watts
    
    print(f"{'Power (MW)':<15} {'Temp Rise (K)':<18} {'Status':<20} {'Notes'}")
    print("-" * 80)
    
    for power in power_levels:
        config = ReactorConfiguration(
            coolant_inlet_temp=base_config.coolant_inlet_temp,
            coolant_flow_rate=base_config.coolant_flow_rate,
            reactor_power=power,
            core_height=base_config.core_height,
            core_diameter=base_config.core_diameter,
            pressure=base_config.pressure
        )
        
        # Estimate temperature rise (simplified)
        temp_rise = power / (config.coolant_flow_rate * 1270.0)  # Sodium Cp
        
        # Validate
        is_valid, messages = ConfigValidator.validate(config)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        
        notes = ""
        if messages:
            if is_valid:
                notes = "Warnings present"
            else:
                notes = f"{len(messages)} errors"
        
        print(f"{power/1e6:<15.2f} {temp_rise:<18.1f} {status:<20} {notes}")


def analyze_flow_rate_sweep():
    """
    Analyze effect of flow rate on reactor performance
    """
    print("\n\nFlow Rate Analysis")
    print("=" * 80)
    print()
    
    reactor_power = 2e6  # 2 MW
    flow_rates = [5.0, 10.0, 15.0, 20.0, 25.0]  # kg/s
    
    print(f"{'Flow (kg/s)':<15} {'Temp Rise (K)':<18} {'Outlet (K)':<15} {'Status'}")
    print("-" * 80)
    
    for flow_rate in flow_rates:
        config = ReactorConfiguration(
            coolant_inlet_temp=600.0,
            coolant_flow_rate=flow_rate,
            reactor_power=reactor_power,
            core_height=2.0,
            core_diameter=0.5,
            pressure=1e7
        )
        
        temp_rise = reactor_power / (flow_rate * 1270.0)
        outlet_temp = config.coolant_inlet_temp + temp_rise
        
        is_valid, messages = ConfigValidator.validate(config)
        status = "✓" if is_valid else "✗"
        
        print(f"{flow_rate:<15.1f} {temp_rise:<18.1f} {outlet_temp:<15.1f} {status}")


def analyze_geometry_effects():
    """
    Analyze effect of core geometry on reactor design
    """
    print("\n\nCore Geometry Analysis")
    print("=" * 80)
    print()
    
    print("Effect of core diameter on flow characteristics:")
    print(f"{'Diameter (m)':<15} {'Area (m²)':<15} {'Velocity (m/s)':<20} {'Notes'}")
    print("-" * 80)
    
    flow_rate = 10.0  # kg/s
    sodium_density = 870.0  # kg/m³ at 600K
    
    diameters = [0.3, 0.4, 0.5, 0.6, 0.8]
    
    for diameter in diameters:
        import math
        area = math.pi * diameter**2 / 4.0
        velocity = flow_rate / (sodium_density * area)
        
        config = ReactorConfiguration(
            coolant_inlet_temp=600.0,
            coolant_flow_rate=flow_rate,
            reactor_power=1e6,
            core_height=2.0,
            core_diameter=diameter,
            pressure=1e7
        )
        
        is_valid, _ = ConfigValidator.validate(config)
        notes = "Good velocity" if 1.0 < velocity < 10.0 else "Consider adjustment"
        if not is_valid:
            notes = "Invalid config"
        
        print(f"{diameter:<15.2f} {area:<15.4f} {velocity:<20.2f} {notes}")


def analyze_temperature_limits():
    """
    Analyze temperature limits and safety margins
    """
    print("\n\nTemperature Safety Analysis")
    print("=" * 80)
    print()
    
    print("Coolant inlet temperature effects:")
    print(f"{'Inlet T (K)':<15} {'Inlet T (°C)':<18} {'Status':<15} {'Notes'}")
    print("-" * 80)
    
    temperatures = [400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    
    for temp in temperatures:
        config = ReactorConfiguration(
            coolant_inlet_temp=temp,
            coolant_flow_rate=10.0,
            reactor_power=1e6,
            core_height=2.0,
            core_diameter=0.5,
            pressure=1e7
        )
        
        is_valid, messages = ConfigValidator.validate(config)
        
        if is_valid:
            status = "✓ Valid"
            if messages:
                notes = "Has warnings"
            else:
                notes = "Optimal"
        else:
            status = "✗ Invalid"
            notes = "Out of range"
        
        temp_c = temp - 273.15
        print(f"{temp:<15.1f} {temp_c:<18.1f} {status:<15} {notes}")


def design_recommendations():
    """
    Provide design recommendations based on analysis
    """
    print("\n\nDesign Recommendations")
    print("=" * 80)
    print()
    
    print("Small Reactor (500 kW - 1 MW):")
    print("  • Recommended flow rate: 5-10 kg/s")
    print("  • Core diameter: 0.3-0.5 m")
    print("  • Core height: 1.0-1.5 m")
    print("  • Inlet temperature: 600-700 K")
    print("  • Applications: Lunar/Mars surface, small spacecraft")
    print()
    
    print("Medium Reactor (1-5 MW):")
    print("  • Recommended flow rate: 10-20 kg/s")
    print("  • Core diameter: 0.5-0.7 m")
    print("  • Core height: 1.5-2.5 m")
    print("  • Inlet temperature: 600-750 K")
    print("  • Applications: Space stations, large habitats")
    print()
    
    print("Large Reactor (5-10 MW):")
    print("  • Recommended flow rate: 20-30 kg/s")
    print("  • Core diameter: 0.7-1.0 m")
    print("  • Core height: 2.0-3.0 m")
    print("  • Inlet temperature: 650-800 K")
    print("  • Applications: Deep space missions, propulsion")
    print()
    
    print("Key Design Considerations:")
    print("  1. Higher flow rates reduce temperature rise but increase pumping power")
    print("  2. Larger diameter cores reduce coolant velocity and pressure drop")
    print("  3. Temperature rise should typically be kept under 150-200 K")
    print("  4. Reynolds number should be >10,000 for good heat transfer")
    print("  5. Pressure drop should be minimized for system efficiency")


def main():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SPLINTHER PARAMETER STUDY" + " " * 33 + "║")
    print("║" + " " * 10 + "Nuclear Reactor Fluid Dynamics Analysis" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Run various analyses
    analyze_power_sweep()
    analyze_flow_rate_sweep()
    analyze_geometry_effects()
    analyze_temperature_limits()
    design_recommendations()
    
    print("\n" + "=" * 80)
    print("\nParameter study complete!")
    print("\nNote: These analyses use simplified models for demonstration.")
    print("For detailed fluid dynamics calculations, use the full Rust calculator.")
    print()


if __name__ == "__main__":
    sys.exit(main() or 0)
