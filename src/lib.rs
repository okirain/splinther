use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

pub mod thermal_hydraulics;
pub mod fluid_dynamics;
pub mod heat_transfer;
pub mod pressure;

/// Configuration for the nuclear reactor
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct ReactorConfig {
    #[pyo3(get, set)]
    pub coolant_inlet_temp: f64,      // Kelvin
    #[pyo3(get, set)]
    pub coolant_flow_rate: f64,       // kg/s
    #[pyo3(get, set)]
    pub reactor_power: f64,           // Watts
    #[pyo3(get, set)]
    pub core_height: f64,             // meters
    #[pyo3(get, set)]
    pub core_diameter: f64,           // meters
    #[pyo3(get, set)]
    pub pressure: f64,                // Pascals
}

#[pymethods]
impl ReactorConfig {
    #[new]
    pub fn new(
        coolant_inlet_temp: f64,
        coolant_flow_rate: f64,
        reactor_power: f64,
        core_height: f64,
        core_diameter: f64,
        pressure: f64,
    ) -> Self {
        ReactorConfig {
            coolant_inlet_temp,
            coolant_flow_rate,
            reactor_power,
            core_height,
            core_diameter,
            pressure,
        }
    }
}

/// Results from fluid dynamics calculations
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct FluidDynamicsResults {
    #[pyo3(get)]
    pub outlet_temperature: f64,
    #[pyo3(get)]
    pub pressure_drop: f64,
    #[pyo3(get)]
    pub reynolds_number: f64,
    #[pyo3(get)]
    pub heat_transfer_coefficient: f64,
    #[pyo3(get)]
    pub max_fuel_temperature: f64,
}

#[pymethods]
impl FluidDynamicsResults {
    fn __repr__(&self) -> String {
        format!(
            "FluidDynamicsResults(outlet_temp={:.2}K, pressure_drop={:.2}Pa, Re={:.2}, h={:.2}W/m²K, max_fuel_temp={:.2}K)",
            self.outlet_temperature,
            self.pressure_drop,
            self.reynolds_number,
            self.heat_transfer_coefficient,
            self.max_fuel_temperature
        )
    }
}

/// Main calculator for nuclear reactor fluid dynamics
#[pyclass]
pub struct ReactorCalculator {
    config: ReactorConfig,
}

#[pymethods]
impl ReactorCalculator {
    #[new]
    pub fn new(config: ReactorConfig) -> Self {
        ReactorCalculator { config }
    }

    /// Perform complete fluid dynamics analysis
    pub fn calculate(&self) -> PyResult<FluidDynamicsResults> {
        // Calculate outlet temperature
        let outlet_temp = thermal_hydraulics::calculate_outlet_temperature(
            self.config.coolant_inlet_temp,
            self.config.reactor_power,
            self.config.coolant_flow_rate,
        );

        // Calculate Reynolds number for flow characterization
        let reynolds = fluid_dynamics::calculate_reynolds_number(
            self.config.coolant_flow_rate,
            self.config.core_diameter,
            self.config.coolant_inlet_temp,
        );

        // Calculate heat transfer coefficient
        let heat_transfer_coef = heat_transfer::calculate_heat_transfer_coefficient(
            reynolds,
            self.config.core_diameter,
            self.config.coolant_inlet_temp,
        );

        // Calculate pressure drop through core
        let pressure_drop = pressure::calculate_pressure_drop(
            self.config.coolant_flow_rate,
            self.config.core_height,
            self.config.core_diameter,
            reynolds,
        );

        // Estimate maximum fuel temperature
        let max_fuel_temp = thermal_hydraulics::calculate_max_fuel_temperature(
            outlet_temp,
            self.config.reactor_power,
            heat_transfer_coef,
            self.config.core_height,
            self.config.core_diameter,
        );

        Ok(FluidDynamicsResults {
            outlet_temperature: outlet_temp,
            pressure_drop,
            reynolds_number: reynolds,
            heat_transfer_coefficient: heat_transfer_coef,
            max_fuel_temperature: max_fuel_temp,
        })
    }

    /// Get current configuration
    pub fn get_config(&self) -> ReactorConfig {
        self.config.clone()
    }

    /// Update configuration
    pub fn update_config(&mut self, config: ReactorConfig) {
        self.config = config;
    }
}

/// Python module initialization
#[pymodule]
fn splinther(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ReactorConfig>()?;
    m.add_class::<FluidDynamicsResults>()?;
    m.add_class::<ReactorCalculator>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reactor_config_creation() {
        let config = ReactorConfig::new(
            600.0,  // inlet temp (K)
            10.0,   // flow rate (kg/s)
            1e6,    // power (W)
            2.0,    // height (m)
            0.5,    // diameter (m)
            1e7,    // pressure (Pa)
        );
        assert_eq!(config.coolant_inlet_temp, 600.0);
        assert_eq!(config.reactor_power, 1e6);
    }

    #[test]
    fn test_calculator_creation() {
        let config = ReactorConfig::new(600.0, 10.0, 1e6, 2.0, 0.5, 1e7);
        let calculator = ReactorCalculator::new(config);
        assert_eq!(calculator.config.reactor_power, 1e6);
    }
}
