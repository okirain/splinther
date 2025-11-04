"""
Tests for Splinther configuration system
"""

import sys
from pathlib import Path
import tempfile
import json

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from splinther_config import (
    ConfigLoader,
    ReactorConfiguration,
    ConfigValidator,
    export_to_json,
    export_to_yaml,
)


def test_reactor_configuration_creation():
    """Test creating a ReactorConfiguration object"""
    config = ReactorConfiguration(
        coolant_inlet_temp=600.0,
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7,
        name="Test Reactor",
        description="Test configuration"
    )
    
    assert config.coolant_inlet_temp == 600.0
    assert config.coolant_flow_rate == 10.0
    assert config.reactor_power == 1e6
    assert config.name == "Test Reactor"


def test_config_to_dict():
    """Test converting configuration to dictionary"""
    config = ReactorConfiguration(
        coolant_inlet_temp=600.0,
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7
    )
    
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert config_dict['coolant_inlet_temp'] == 600.0
    assert config_dict['reactor_power'] == 1e6


def test_config_from_dict():
    """Test creating configuration from dictionary"""
    data = {
        'coolant_inlet_temp': 650.0,
        'coolant_flow_rate': 15.0,
        'reactor_power': 2e6,
        'core_height': 2.5,
        'core_diameter': 0.6,
        'pressure': 1.5e7
    }
    
    config = ReactorConfiguration.from_dict(data)
    assert config.coolant_inlet_temp == 650.0
    assert config.reactor_power == 2e6


def test_load_yaml():
    """Test loading configuration from YAML file"""
    config_path = Path(__file__).parent.parent.parent / "configs" / "small_reactor.yaml"
    config = ConfigLoader.load_yaml(str(config_path))
    
    assert config.name == "Small Space Reactor"
    assert config.coolant_inlet_temp == 600.0
    assert config.reactor_power == 500000.0


def test_load_json():
    """Test loading configuration from JSON file"""
    config_path = Path(__file__).parent.parent.parent / "configs" / "example_reactor.json"
    config = ConfigLoader.load_json(str(config_path))
    
    assert config.name == "Example Reactor"
    assert config.coolant_inlet_temp == 650.0
    assert config.reactor_power == 1000000.0


def test_auto_load():
    """Test auto-detecting file format"""
    yaml_path = Path(__file__).parent.parent.parent / "configs" / "small_reactor.yaml"
    config_yaml = ConfigLoader.load(str(yaml_path))
    assert config_yaml.name == "Small Space Reactor"
    
    json_path = Path(__file__).parent.parent.parent / "configs" / "example_reactor.json"
    config_json = ConfigLoader.load(str(json_path))
    assert config_json.name == "Example Reactor"


def test_save_and_load_json():
    """Test saving and loading JSON configuration"""
    config = ReactorConfiguration(
        coolant_inlet_temp=700.0,
        coolant_flow_rate=12.0,
        reactor_power=1.5e6,
        core_height=2.2,
        core_diameter=0.55,
        pressure=1.2e7,
        name="Test Save"
    )
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        ConfigLoader.save_json(config, temp_path)
        loaded_config = ConfigLoader.load_json(temp_path)
        
        assert loaded_config.coolant_inlet_temp == 700.0
        assert loaded_config.reactor_power == 1.5e6
        assert loaded_config.name == "Test Save"
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_validation_valid_config():
    """Test validation of a valid configuration"""
    config = ReactorConfiguration(
        coolant_inlet_temp=600.0,
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7
    )
    
    is_valid, messages = ConfigValidator.validate(config)
    assert is_valid is True


def test_validation_invalid_temperature():
    """Test validation catches invalid temperature"""
    config = ReactorConfiguration(
        coolant_inlet_temp=100.0,  # Too low
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7
    )
    
    is_valid, messages = ConfigValidator.validate(config)
    assert is_valid is False
    assert len(messages) > 0


def test_validation_invalid_power():
    """Test validation catches invalid power"""
    config = ReactorConfiguration(
        coolant_inlet_temp=600.0,
        coolant_flow_rate=10.0,
        reactor_power=100.0,  # Too low
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7
    )
    
    is_valid, messages = ConfigValidator.validate(config)
    assert is_valid is False


def test_validation_warnings():
    """Test validation generates warnings for edge cases"""
    config = ReactorConfiguration(
        coolant_inlet_temp=350.0,  # Low but valid
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7
    )
    
    is_valid, messages = ConfigValidator.validate(config)
    # Should be valid but have warnings
    assert is_valid is True
    assert len(messages) > 0


def test_export_to_json():
    """Test exporting configuration to JSON"""
    config = ReactorConfiguration(
        coolant_inlet_temp=600.0,
        coolant_flow_rate=10.0,
        reactor_power=1e6,
        core_height=2.0,
        core_diameter=0.5,
        pressure=1e7
    )
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        export_to_json(config, temp_path)
        
        # Verify file was created and contains valid JSON
        with open(temp_path, 'r') as f:
            data = json.load(f)
        
        assert data['coolant_inlet_temp'] == 600.0
        assert data['reactor_power'] == 1e6
    finally:
        Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    # Run basic tests
    test_reactor_configuration_creation()
    test_config_to_dict()
    test_config_from_dict()
    test_load_yaml()
    test_load_json()
    test_auto_load()
    test_save_and_load_json()
    test_validation_valid_config()
    test_validation_invalid_temperature()
    test_validation_invalid_power()
    test_validation_warnings()
    test_export_to_json()
    
    print("All tests passed!")
