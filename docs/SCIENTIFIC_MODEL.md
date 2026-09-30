# Scientific Model Specification

## Purpose

This document is the source of truth for scientific assumptions used by the prototype.

## Model

The real simulation engine is ANUGA hydrodynamic modelling.

## Required Inputs

- Terrain/elevation
- Computational domain
- Initial water condition
- Boundary conditions
- Dam/breach representation
- Simulation duration
- Spatial and temporal resolution choices

## Outputs

At minimum:
- water depth
- flood extent

Where available:
- velocity
- stage/elevation
- time-dependent output

## Assumptions

All assumptions must be explicit in the implementation and UI.

Examples:
- DEM resolution
- Manning roughness values
- breach geometry
- initial reservoir condition
- downstream boundary condition
- time step/output interval

Do not hide scientific assumptions inside arbitrary constants.

## Validation

The prototype should distinguish:
- model output,
- validation result,
- illustrative/demo output.

If no ground-truth event is available, do not claim model accuracy.

## Limitations

Results are sensitive to terrain quality, breach assumptions, hydraulic parameters, domain selection and input data quality.
