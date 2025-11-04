"""
Export utilities for reactor configurations and results
"""

import json
import yaml
from typing import Any, Dict
from .config_loader import ReactorConfiguration


def export_to_json(data: Any, filepath: str, indent: int = 2):
    """
    Export data to JSON file
    
    Args:
        data: Data to export (dict, ReactorConfiguration, or JSON-serializable object)
        filepath: Destination file path
        indent: JSON indentation level
    """
    if isinstance(data, ReactorConfiguration):
        data = data.to_dict()
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def export_to_yaml(data: Any, filepath: str):
    """
    Export data to YAML file
    
    Args:
        data: Data to export (dict, ReactorConfiguration, or YAML-serializable object)
        filepath: Destination file path
    """
    if isinstance(data, ReactorConfiguration):
        data = data.to_dict()
    
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def format_results(results: Dict[str, float]) -> str:
    """
    Format calculation results for display
    
    Args:
        results: Dictionary of calculation results
        
    Returns:
        Formatted string
    """
    lines = ["Reactor Fluid Dynamics Results", "=" * 40]
    
    for key, value in results.items():
        # Format key nicely
        formatted_key = key.replace('_', ' ').title()
        
        # Format value with appropriate units
        if 'temperature' in key.lower():
            lines.append(f"{formatted_key}: {value:.2f} K ({value - 273.15:.2f} °C)")
        elif 'pressure' in key.lower():
            lines.append(f"{formatted_key}: {value:.2e} Pa ({value/1e5:.2f} bar)")
        elif 'reynolds' in key.lower():
            lines.append(f"{formatted_key}: {value:.2e}")
        elif 'coefficient' in key.lower():
            lines.append(f"{formatted_key}: {value:.2f} W/m²·K")
        else:
            lines.append(f"{formatted_key}: {value:.2e}")
    
    return "\n".join(lines)
