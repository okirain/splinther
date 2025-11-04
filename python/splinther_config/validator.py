"""
Configuration validation for nuclear reactor parameters
Ensures physical constraints and safety limits are met
"""

from typing import List, Tuple
from .config_loader import ReactorConfiguration


class ValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


class ConfigValidator:
    """Validator for reactor configuration parameters"""
    
    # Physical constraints for space nuclear reactors
    MIN_TEMP = 273.15  # 0°C in Kelvin (absolute minimum, coolant freezing)
    MAX_TEMP = 1500.0  # Maximum reasonable coolant temp (K)
    
    MIN_FLOW_RATE = 0.1  # kg/s (minimum practical flow)
    MAX_FLOW_RATE = 1000.0  # kg/s (maximum reasonable for space reactors)
    
    MIN_POWER = 1e3  # 1 kW (minimum useful power)
    MAX_POWER = 1e8  # 100 MW (maximum for space reactors)
    
    MIN_DIMENSION = 0.01  # 1 cm (minimum practical dimension)
    MAX_DIMENSION = 10.0  # 10 m (maximum reasonable for space)
    
    MIN_PRESSURE = 1e3  # 1 kPa (minimum practical)
    MAX_PRESSURE = 1e8  # 1000 bar (maximum reasonable)
    
    @classmethod
    def validate(cls, config: ReactorConfiguration, strict: bool = False) -> Tuple[bool, List[str]]:
        """
        Validate reactor configuration
        
        Args:
            config: ReactorConfiguration to validate
            strict: If True, warnings are treated as errors
            
        Returns:
            Tuple of (is_valid, list of error/warning messages)
        """
        errors = []
        warnings = []
        
        # Validate temperature
        if config.coolant_inlet_temp < cls.MIN_TEMP:
            errors.append(
                f"Coolant inlet temperature ({config.coolant_inlet_temp}K) "
                f"below minimum ({cls.MIN_TEMP}K)"
            )
        elif config.coolant_inlet_temp < 400.0:
            warnings.append(
                f"Coolant inlet temperature ({config.coolant_inlet_temp}K) "
                f"is unusually low for liquid metal coolants"
            )
        
        if config.coolant_inlet_temp > cls.MAX_TEMP:
            errors.append(
                f"Coolant inlet temperature ({config.coolant_inlet_temp}K) "
                f"exceeds maximum ({cls.MAX_TEMP}K)"
            )
        
        # Validate flow rate
        if config.coolant_flow_rate < cls.MIN_FLOW_RATE:
            errors.append(
                f"Coolant flow rate ({config.coolant_flow_rate} kg/s) "
                f"below minimum ({cls.MIN_FLOW_RATE} kg/s)"
            )
        
        if config.coolant_flow_rate > cls.MAX_FLOW_RATE:
            errors.append(
                f"Coolant flow rate ({config.coolant_flow_rate} kg/s) "
                f"exceeds maximum ({cls.MAX_FLOW_RATE} kg/s)"
            )
        
        # Validate reactor power
        if config.reactor_power < cls.MIN_POWER:
            errors.append(
                f"Reactor power ({config.reactor_power} W) "
                f"below minimum ({cls.MIN_POWER} W)"
            )
        
        if config.reactor_power > cls.MAX_POWER:
            errors.append(
                f"Reactor power ({config.reactor_power} W) "
                f"exceeds maximum ({cls.MAX_POWER} W)"
            )
        
        # Validate dimensions
        if config.core_height < cls.MIN_DIMENSION:
            errors.append(
                f"Core height ({config.core_height} m) "
                f"below minimum ({cls.MIN_DIMENSION} m)"
            )
        
        if config.core_height > cls.MAX_DIMENSION:
            errors.append(
                f"Core height ({config.core_height} m) "
                f"exceeds maximum ({cls.MAX_DIMENSION} m)"
            )
        
        if config.core_diameter < cls.MIN_DIMENSION:
            errors.append(
                f"Core diameter ({config.core_diameter} m) "
                f"below minimum ({cls.MIN_DIMENSION} m)"
            )
        
        if config.core_diameter > cls.MAX_DIMENSION:
            errors.append(
                f"Core diameter ({config.core_diameter} m) "
                f"exceeds maximum ({cls.MAX_DIMENSION} m)"
            )
        
        # Validate pressure
        if config.pressure < cls.MIN_PRESSURE:
            errors.append(
                f"System pressure ({config.pressure} Pa) "
                f"below minimum ({cls.MIN_PRESSURE} Pa)"
            )
        
        if config.pressure > cls.MAX_PRESSURE:
            errors.append(
                f"System pressure ({config.pressure} Pa) "
                f"exceeds maximum ({cls.MAX_PRESSURE} Pa)"
            )
        
        # Check thermal balance (warning only)
        expected_temp_rise = config.reactor_power / (config.coolant_flow_rate * 1270.0)  # Sodium Cp
        if expected_temp_rise > 200.0:
            warnings.append(
                f"Large temperature rise expected ({expected_temp_rise:.1f}K). "
                f"Consider increasing flow rate."
            )
        
        # Combine messages
        all_messages = errors + warnings
        
        if strict:
            is_valid = len(all_messages) == 0
        else:
            is_valid = len(errors) == 0
        
        return is_valid, all_messages
    
    @classmethod
    def validate_strict(cls, config: ReactorConfiguration) -> None:
        """
        Validate configuration in strict mode
        Raises ValidationError if any issues found
        
        Args:
            config: ReactorConfiguration to validate
            
        Raises:
            ValidationError: If validation fails
        """
        is_valid, messages = cls.validate(config, strict=True)
        if not is_valid:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {m}" for m in messages)
            raise ValidationError(error_msg)
