/// Heat transfer calculations for nuclear reactor
use crate::fluid_dynamics;

/// Thermal conductivity of liquid sodium (W/m·K)
pub fn sodium_thermal_conductivity(temperature: f64) -> f64 {
    // Empirical correlation for liquid sodium
    // k ≈ 86 W/m·K at typical reactor temperatures
    let temp_celsius = temperature - 273.15;
    86.0 - 0.047 * temp_celsius
}

/// Prandtl number for liquid sodium
/// 
/// Pr = (cp * μ) / k
pub fn calculate_prandtl_number(temperature: f64) -> f64 {
    const SODIUM_CP: f64 = 1270.0; // J/kg·K
    let viscosity = fluid_dynamics::sodium_viscosity(temperature);
    let thermal_cond = sodium_thermal_conductivity(temperature);
    
    (SODIUM_CP * viscosity) / thermal_cond
}

/// Calculate Nusselt number using appropriate correlation
/// 
/// # Arguments
/// * `reynolds` - Reynolds number
/// * `prandtl` - Prandtl number
/// * `flow_type` - Type of flow ("turbulent" or "laminar")
/// 
/// # Returns
/// Nusselt number (dimensionless)
pub fn calculate_nusselt_number(reynolds: f64, prandtl: f64) -> f64 {
    if reynolds < 2300.0 {
        // Laminar flow - constant Nusselt for fully developed flow
        3.66
    } else if reynolds > 4000.0 {
        // Turbulent flow - Dittus-Boelter correlation
        // Nu = 0.023 * Re^0.8 * Pr^0.4 (for heating)
        0.023 * reynolds.powf(0.8) * prandtl.powf(0.4)
    } else {
        // Transition region - interpolate
        let nu_lam = 3.66;
        let nu_turb = 0.023 * 4000.0_f64.powf(0.8) * prandtl.powf(0.4);
        nu_lam + (nu_turb - nu_lam) * (reynolds - 2300.0) / 1700.0
    }
}

/// Calculate heat transfer coefficient
/// 
/// # Arguments
/// * `reynolds` - Reynolds number
/// * `diameter` - Hydraulic diameter in meters
/// * `temperature` - Coolant temperature in Kelvin
/// 
/// # Returns
/// Heat transfer coefficient in W/m²·K
pub fn calculate_heat_transfer_coefficient(
    reynolds: f64,
    diameter: f64,
    temperature: f64,
) -> f64 {
    let prandtl = calculate_prandtl_number(temperature);
    let nusselt = calculate_nusselt_number(reynolds, prandtl);
    let thermal_cond = sodium_thermal_conductivity(temperature);
    
    // h = Nu * k / D
    (nusselt * thermal_cond) / diameter
}

/// Calculate heat flux based on power and surface area
/// 
/// # Arguments
/// * `power` - Total thermal power in Watts
/// * `surface_area` - Heat transfer surface area in m²
/// 
/// # Returns
/// Heat flux in W/m²
pub fn calculate_heat_flux(power: f64, surface_area: f64) -> f64 {
    power / surface_area
}

/// Calculate required surface area for heat removal
/// 
/// # Arguments
/// * `power` - Total thermal power in Watts
/// * `heat_transfer_coef` - Heat transfer coefficient in W/m²·K
/// * `temp_difference` - Temperature difference between surface and fluid in K
/// 
/// # Returns
/// Required surface area in m²
pub fn calculate_required_area(
    power: f64,
    heat_transfer_coef: f64,
    temp_difference: f64,
) -> f64 {
    power / (heat_transfer_coef * temp_difference)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sodium_thermal_conductivity() {
        let k = sodium_thermal_conductivity(600.0);
        // Should be around 70-80 W/m·K at 600K
        assert!(k > 60.0 && k < 90.0);
    }

    #[test]
    fn test_prandtl_number() {
        let pr = calculate_prandtl_number(600.0);
        // Liquid sodium has very low Prandtl number (typically 0.003-0.08)
        assert!(pr > 0.001 && pr < 0.1);
    }

    #[test]
    fn test_nusselt_laminar() {
        let nu = calculate_nusselt_number(1000.0, 0.01);
        assert_eq!(nu, 3.66); // Constant for laminar flow
    }

    #[test]
    fn test_nusselt_turbulent() {
        let nu = calculate_nusselt_number(50000.0, 0.01);
        // Should be much higher than laminar
        assert!(nu > 10.0);
    }

    #[test]
    fn test_heat_transfer_coefficient() {
        let h = calculate_heat_transfer_coefficient(50000.0, 0.5, 600.0);
        // Should be reasonable value (thousands of W/m²K for liquid metal)
        assert!(h > 1000.0 && h < 100000.0);
    }

    #[test]
    fn test_heat_flux() {
        let flux = calculate_heat_flux(1e6, 10.0);
        assert_eq!(flux, 1e5); // 100 kW/m²
    }

    #[test]
    fn test_required_area() {
        let area = calculate_required_area(1e6, 10000.0, 100.0);
        assert_eq!(area, 1.0); // 1 m²
    }
}
