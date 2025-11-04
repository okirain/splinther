"""
Configuration loader for nuclear reactor parameters
Supports YAML and JSON configuration files
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ReactorConfiguration:
    """
    Nuclear reactor configuration parameters
    
    Attributes:
        coolant_inlet_temp: Coolant inlet temperature (Kelvin)
        coolant_flow_rate: Mass flow rate (kg/s)
        reactor_power: Thermal power output (Watts)
        core_height: Height of reactor core (meters)
        core_diameter: Diameter of reactor core (meters)
        pressure: System pressure (Pascals)
        name: Optional reactor name
        description: Optional description
    """
    coolant_inlet_temp: float
    coolant_flow_rate: float
    reactor_power: float
    core_height: float
    core_diameter: float
    pressure: float
    name: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReactorConfiguration':
        """Create configuration from dictionary"""
        return cls(**data)


class ConfigLoader:
    """Loader for reactor configuration files"""
    
    @staticmethod
    def load_yaml(filepath: str) -> ReactorConfiguration:
        """
        Load configuration from YAML file
        
        Args:
            filepath: Path to YAML configuration file
            
        Returns:
            ReactorConfiguration object
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        return ReactorConfiguration.from_dict(data)
    
    @staticmethod
    def load_json(filepath: str) -> ReactorConfiguration:
        """
        Load configuration from JSON file
        
        Args:
            filepath: Path to JSON configuration file
            
        Returns:
            ReactorConfiguration object
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        return ReactorConfiguration.from_dict(data)
    
    @staticmethod
    def load(filepath: str) -> ReactorConfiguration:
        """
        Auto-detect and load configuration file
        
        Args:
            filepath: Path to configuration file (YAML or JSON)
            
        Returns:
            ReactorConfiguration object
        """
        path = Path(filepath)
        suffix = path.suffix.lower()
        
        if suffix in ['.yaml', '.yml']:
            return ConfigLoader.load_yaml(filepath)
        elif suffix == '.json':
            return ConfigLoader.load_json(filepath)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .yaml, .yml, or .json")
    
    @staticmethod
    def save_yaml(config: ReactorConfiguration, filepath: str):
        """
        Save configuration to YAML file
        
        Args:
            config: ReactorConfiguration object
            filepath: Destination file path
        """
        with open(filepath, 'w') as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def save_json(config: ReactorConfiguration, filepath: str, indent: int = 2):
        """
        Save configuration to JSON file
        
        Args:
            config: ReactorConfiguration object
            filepath: Destination file path
            indent: JSON indentation level
        """
        with open(filepath, 'w') as f:
            json.dump(config.to_dict(), f, indent=indent)
