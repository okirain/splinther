/// Fluid dynamics calculations for reactor coolant flow
use std::f64::consts::PI;

/// Properties of liquid sodium coolant at typical operating conditions
/// Density as function of temperature (kg/m³)
pub fn sodium_density(temperature: f64) -> f64 {
    // Empirical correlation for liquid sodium
    // ρ = 1014 - 0.235 * (T - 273.15)
    1014.0 - 0.235 * (temperature - 273.15)
}

/// Dynamic viscosity of liquid sodium (Pa·s)
pub fn sodium_viscosity(temperature: f64) -> f64 {
    // Empirical correlation for liquid sodium
    // μ ≈ 0.001 Pa·s at typical reactor temperatures
    let temp_celsius = temperature - 273.15;
    0.001 * (-2.45e-4 * temp_celsius + 1.0).exp()
}

/// Calculate Reynolds number for flow characterization
/// 
/// # Arguments
/// * `flow_rate` - Mass flow rate in kg/s
/// * `diameter` - Hydraulic diameter in meters
/// * `temperature` - Coolant temperature in Kelvin
/// 
/// # Returns
/// Reynolds number (dimensionless)
pub fn calculate_reynolds_number(flow_rate: f64, diameter: f64, temperature: f64) -> f64 {
    let density = sodium_density(temperature);
    let viscosity = sodium_viscosity(temperature);
    let area = PI * diameter * diameter / 4.0;
    let velocity = flow_rate / (density * area);
    
    // Re = ρ * V * D / μ
    (density * velocity * diameter) / viscosity
}

/// Calculate flow velocity
/// 
/// # Arguments
/// * `flow_rate` - Mass flow rate in kg/s
/// * `diameter` - Hydraulic diameter in meters
/// * `temperature` - Coolant temperature in Kelvin
/// 
/// # Returns
/// Flow velocity in m/s
pub fn calculate_velocity(flow_rate: f64, diameter: f64, temperature: f64) -> f64 {
    let density = sodium_density(temperature);
    let area = PI * diameter * diameter / 4.0;
    flow_rate / (density * area)
}

/// Determine if flow is laminar or turbulent
/// 
/// # Returns
/// true if turbulent (Re > 4000), false if laminar
pub fn is_turbulent(reynolds: f64) -> bool {
    reynolds > 4000.0
}

/// Calculate friction factor using appropriate correlation
/// 
/// # Arguments
/// * `reynolds` - Reynolds number
/// 
/// # Returns
/// Darcy friction factor (dimensionless)
pub fn calculate_friction_factor(reynolds: f64) -> f64 {
    if reynolds < 2300.0 {
        // Laminar flow
        64.0 / reynolds
    } else if reynolds < 4000.0 {
        // Transition region - linear interpolation
        let f_lam = 64.0 / 2300.0;
        let f_turb = 0.316 / reynolds.powf(0.25);
        f_lam + (f_turb - f_lam) * (reynolds - 2300.0) / 1700.0
    } else {
        // Turbulent flow - Blasius correlation
        0.316 / reynolds.powf(0.25)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sodium_density() {
        let density = sodium_density(600.0); // 600 K
        // Should be around 870 kg/m³ at 600K
        assert!(density > 800.0 && density < 950.0);
    }

    #[test]
    fn test_sodium_viscosity() {
        let viscosity = sodium_viscosity(600.0);
        // Should be around 0.001 Pa·s
        assert!(viscosity > 0.0001 && viscosity < 0.01);
    }

    #[test]
    fn test_reynolds_number() {
        let re = calculate_reynolds_number(10.0, 0.5, 600.0);
        // Should be turbulent (Re > 4000) for typical reactor conditions
        assert!(re > 4000.0);
    }

    #[test]
    fn test_is_turbulent() {
        assert!(is_turbulent(10000.0));
        assert!(!is_turbulent(2000.0));
    }

    #[test]
    fn test_friction_factor_laminar() {
        let f = calculate_friction_factor(1000.0);
        assert_eq!(f, 64.0 / 1000.0);
    }

    #[test]
    fn test_friction_factor_turbulent() {
        let f = calculate_friction_factor(10000.0);
        let expected = 0.316 / 10000.0_f64.powf(0.25);
        assert!((f - expected).abs() < 1e-6);
    }

    #[test]
    fn test_calculate_velocity() {
        let velocity = calculate_velocity(10.0, 0.5, 600.0);
        // Should be reasonable velocity (few m/s)
        assert!(velocity > 0.0 && velocity < 50.0);
    }
}
