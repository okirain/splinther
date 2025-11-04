/// Thermal hydraulics calculations for nuclear reactor coolant
use std::f64::consts::PI;
use crate::constants::{SODIUM_CP, FUEL_TEMP_RISE_FACTOR};

/// Calculate outlet temperature of coolant
/// 
/// # Arguments
/// * `inlet_temp` - Inlet temperature in Kelvin
/// * `power` - Reactor thermal power in Watts
/// * `flow_rate` - Mass flow rate in kg/s
/// 
/// # Returns
/// Outlet temperature in Kelvin
pub fn calculate_outlet_temperature(inlet_temp: f64, power: f64, flow_rate: f64) -> f64 {
    // Q = m * cp * ΔT
    // ΔT = Q / (m * cp)
    let delta_t = power / (flow_rate * SODIUM_CP);
    inlet_temp + delta_t
}

/// Calculate maximum fuel temperature in the reactor core
/// 
/// # Arguments
/// * `coolant_temp` - Average coolant temperature in Kelvin
/// * `power` - Reactor thermal power in Watts
/// * `heat_transfer_coef` - Heat transfer coefficient in W/m²·K
/// * `core_height` - Height of reactor core in meters
/// * `core_diameter` - Diameter of reactor core in meters
/// 
/// # Returns
/// Maximum fuel temperature in Kelvin
pub fn calculate_max_fuel_temperature(
    coolant_temp: f64,
    power: f64,
    heat_transfer_coef: f64,
    core_height: f64,
    core_diameter: f64,
) -> f64 {
    // Calculate heat flux
    let surface_area = PI * core_diameter * core_height;
    let heat_flux = power / surface_area;
    
    // Temperature rise across clad and gap
    // Using simplified model: ΔT = q" / h
    let temp_rise = heat_flux / heat_transfer_coef;
    
    // Add fuel centerline temperature rise (simplified)
    // Assumes linear heat generation with thermal conductivity effects
    let fuel_temp_rise = temp_rise * FUEL_TEMP_RISE_FACTOR;
    
    coolant_temp + fuel_temp_rise
}

/// Calculate average coolant temperature
pub fn calculate_average_coolant_temp(inlet_temp: f64, outlet_temp: f64) -> f64 {
    (inlet_temp + outlet_temp) / 2.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_outlet_temperature() {
        let inlet = 600.0; // K
        let power = 1e6;   // 1 MW
        let flow = 10.0;   // kg/s
        
        let outlet = calculate_outlet_temperature(inlet, power, flow);
        
        // Expected: 600 + 1e6/(10*1270) ≈ 678.7 K
        assert!((outlet - 678.7).abs() < 1.0);
    }

    #[test]
    fn test_max_fuel_temperature() {
        let coolant_temp = 650.0;
        let power = 1e6;
        let h = 10000.0; // W/m²K
        let height = 2.0;
        let diameter = 0.5;
        
        let max_temp = calculate_max_fuel_temperature(
            coolant_temp, power, h, height, diameter
        );
        
        // Should be significantly higher than coolant temp
        assert!(max_temp > coolant_temp);
        assert!(max_temp < 2000.0); // Reasonable upper bound
    }

    #[test]
    fn test_average_temperature() {
        let avg = calculate_average_coolant_temp(600.0, 700.0);
        assert_eq!(avg, 650.0);
    }
}
