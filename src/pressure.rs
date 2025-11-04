/// Pressure drop calculations for reactor coolant system
use std::f64::consts::PI;
use crate::fluid_dynamics;

/// Calculate pressure drop through reactor core
/// 
/// Uses Darcy-Weisbach equation: ΔP = f * (L/D) * (ρ * V²/2)
/// 
/// # Arguments
/// * `flow_rate` - Mass flow rate in kg/s
/// * `length` - Flow path length (core height) in meters
/// * `diameter` - Hydraulic diameter in meters
/// * `reynolds` - Reynolds number
/// * `temperature` - Average coolant temperature in Kelvin (for property evaluation)
/// 
/// # Returns
/// Pressure drop in Pascals
pub fn calculate_pressure_drop(
    flow_rate: f64,
    length: f64,
    diameter: f64,
    reynolds: f64,
    temperature: f64,
) -> f64 {
    // Get friction factor
    let friction_factor = fluid_dynamics::calculate_friction_factor(reynolds);
    
    let density = fluid_dynamics::sodium_density(temperature);
    
    // Calculate velocity
    let area = PI * diameter * diameter / 4.0;
    let velocity = flow_rate / (density * area);
    
    // Darcy-Weisbach equation
    friction_factor * (length / diameter) * (density * velocity * velocity / 2.0)
}

/// Calculate pressure drop due to elevation change (gravity)
/// 
/// ΔP = ρ * g * Δh
/// 
/// # Arguments
/// * `height_change` - Elevation change in meters (positive = upward)
/// * `temperature` - Coolant temperature in Kelvin
/// * `gravity` - Gravitational acceleration in m/s² (use constants::GRAVITY_*)
/// 
/// # Returns
/// Pressure drop in Pascals
pub fn calculate_elevation_pressure_drop(height_change: f64, temperature: f64, gravity: f64) -> f64 {
    let density = fluid_dynamics::sodium_density(temperature);
    
    density * gravity * height_change
}

/// Calculate pressure drop due to flow acceleration/deceleration
/// 
/// ΔP = ρ * (V₂² - V₁²) / 2
/// 
/// # Arguments
/// * `velocity_1` - Initial velocity in m/s
/// * `velocity_2` - Final velocity in m/s
/// * `temperature` - Coolant temperature in Kelvin
/// 
/// # Returns
/// Pressure change in Pascals (negative means pressure increase)
pub fn calculate_acceleration_pressure_drop(
    velocity_1: f64,
    velocity_2: f64,
    temperature: f64,
) -> f64 {
    let density = fluid_dynamics::sodium_density(temperature);
    density * (velocity_2 * velocity_2 - velocity_1 * velocity_1) / 2.0
}

/// Calculate total system pressure drop
/// 
/// Includes friction, elevation, and acceleration effects
/// 
/// # Arguments
/// * `friction_drop` - Pressure drop due to friction in Pa
/// * `elevation_drop` - Pressure drop due to elevation in Pa
/// * `acceleration_drop` - Pressure drop due to acceleration in Pa
/// * `form_loss_coefficient` - K factor for form losses (dimensionless)
/// * `dynamic_pressure` - ρV²/2 in Pa
/// 
/// # Returns
/// Total pressure drop in Pascals
pub fn calculate_total_pressure_drop(
    friction_drop: f64,
    elevation_drop: f64,
    acceleration_drop: f64,
    form_loss_coefficient: f64,
    dynamic_pressure: f64,
) -> f64 {
    friction_drop + elevation_drop + acceleration_drop + 
    (form_loss_coefficient * dynamic_pressure)
}

/// Calculate pump power required to overcome pressure drop
/// 
/// P = ΔP * Q / η
/// 
/// # Arguments
/// * `pressure_drop` - Total pressure drop in Pa
/// * `volumetric_flow_rate` - Flow rate in m³/s
/// * `efficiency` - Pump efficiency (0-1)
/// 
/// # Returns
/// Required pump power in Watts
pub fn calculate_pump_power(
    pressure_drop: f64,
    volumetric_flow_rate: f64,
    efficiency: f64,
) -> f64 {
    (pressure_drop * volumetric_flow_rate) / efficiency
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pressure_drop() {
        let flow_rate = 10.0; // kg/s
        let length = 2.0;     // m
        let diameter = 0.5;   // m
        let reynolds = 50000.0;
        let temperature = 650.0; // K
        
        let dp = calculate_pressure_drop(flow_rate, length, diameter, reynolds, temperature);
        
        // Should be positive
        assert!(dp > 0.0);
        // Should be reasonable (few kPa to hundreds of kPa)
        assert!(dp < 1e6);
    }

    #[test]
    fn test_elevation_pressure_drop() {
        use crate::constants::GRAVITY_EARTH;
        let dp = calculate_elevation_pressure_drop(2.0, 600.0, GRAVITY_EARTH);
        // Should be positive for upward flow
        assert!(dp > 0.0);
        // Roughly ρ*g*h = 870 * 9.81 * 2 ≈ 17 kPa
        assert!(dp > 10000.0 && dp < 25000.0);
    }
    
    #[test]
    fn test_elevation_pressure_drop_different_gravity() {
        use crate::constants::{GRAVITY_MOON, GRAVITY_MARS};
        
        // Test on Moon (lower gravity)
        let dp_moon = calculate_elevation_pressure_drop(2.0, 600.0, GRAVITY_MOON);
        assert!(dp_moon > 0.0);
        assert!(dp_moon < 5000.0); // Should be much less than Earth
        
        // Test on Mars
        let dp_mars = calculate_elevation_pressure_drop(2.0, 600.0, GRAVITY_MARS);
        assert!(dp_mars > 0.0);
        assert!(dp_mars > dp_moon && dp_mars < 10000.0);
    }

    #[test]
    fn test_acceleration_pressure_drop() {
        let dp = calculate_acceleration_pressure_drop(1.0, 2.0, 600.0);
        // Should be positive (pressure drop when accelerating)
        assert!(dp > 0.0);
    }

    #[test]
    fn test_deceleration_pressure_rise() {
        let dp = calculate_acceleration_pressure_drop(2.0, 1.0, 600.0);
        // Should be negative (pressure rise when decelerating)
        assert!(dp < 0.0);
    }

    #[test]
    fn test_total_pressure_drop() {
        let total = calculate_total_pressure_drop(
            10000.0,  // friction
            5000.0,   // elevation
            1000.0,   // acceleration
            1.5,      // form loss K
            2000.0,   // dynamic pressure
        );
        
        // Should sum all components
        assert_eq!(total, 10000.0 + 5000.0 + 1000.0 + 1.5 * 2000.0);
    }

    #[test]
    fn test_pump_power() {
        let power = calculate_pump_power(100000.0, 0.01, 0.8);
        // P = 100000 * 0.01 / 0.8 = 1250 W
        assert_eq!(power, 1250.0);
    }
}
