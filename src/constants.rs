/// Physical constants and material properties for nuclear reactor calculations

/// Specific heat capacity of liquid sodium (J/kg·K)
/// Reference: Fink, J.K., Leibowitz, L. (1995). "Thermodynamic and Transport Properties of Sodium Liquid and Vapor"
pub const SODIUM_CP: f64 = 1270.0;

/// Empirical factor for fuel pellet temperature rise
/// Accounts for thermal resistance through fuel pellet, gap, and cladding
/// Typical values range from 2.0-3.0 depending on geometry
/// Reference: Todreas, N.E., Kazimi, M.S. (2012). "Nuclear Systems Volume I"
pub const FUEL_TEMP_RISE_FACTOR: f64 = 2.5;

/// Base viscosity coefficient for liquid sodium (Pa·s)
/// Reference: Fink-Leibowitz correlation
pub const SODIUM_VISCOSITY_BASE: f64 = 0.001;

/// Temperature coefficient for sodium viscosity correlation (1/K)
pub const SODIUM_VISCOSITY_TEMP_COEF: f64 = -2.45e-4;

/// Gravitational acceleration constants for different environments

/// Standard Earth gravity (m/s²)
pub const GRAVITY_EARTH: f64 = 9.81;

/// Moon surface gravity (m/s²)
pub const GRAVITY_MOON: f64 = 1.62;

/// Mars surface gravity (m/s²)
pub const GRAVITY_MARS: f64 = 3.71;

/// Microgravity (for space applications, m/s²)
pub const GRAVITY_SPACE: f64 = 0.0;

/// Get gravity for a specific environment
pub fn get_gravity(environment: &str) -> f64 {
    match environment.to_lowercase().as_str() {
        "earth" => GRAVITY_EARTH,
        "moon" | "lunar" => GRAVITY_MOON,
        "mars" => GRAVITY_MARS,
        "space" | "microgravity" => GRAVITY_SPACE,
        _ => GRAVITY_EARTH, // Default to Earth
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_constants_defined() {
        assert!(SODIUM_CP > 0.0);
        assert!(FUEL_TEMP_RISE_FACTOR > 0.0);
        assert!(GRAVITY_EARTH > 0.0);
    }

    #[test]
    fn test_get_gravity() {
        assert_eq!(get_gravity("earth"), GRAVITY_EARTH);
        assert_eq!(get_gravity("Moon"), GRAVITY_MOON);
        assert_eq!(get_gravity("MARS"), GRAVITY_MARS);
        assert_eq!(get_gravity("space"), GRAVITY_SPACE);
        assert_eq!(get_gravity("unknown"), GRAVITY_EARTH); // Default
    }
}
