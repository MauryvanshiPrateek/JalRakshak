# Data Contracts

## Scenario

```python
{
    "scenario_id": "demo-medium",
    "dam_id": "demo-dam",
    "breach_width_m": 30.0,
    "breach_depth_m": 15.0,
    "formation_time_min": 10.0,
    "duration_min": 60.0
}
```

## Simulation Result

```python
{
    "simulation_id": "uuid",
    "status": "completed",
    "duration_min": 60,
    "max_water_depth_m": None,
    "max_velocity_mps": None,
    "flooded_area_km2": None,
    "depth_layer": "outputs/depth.tif",
    "extent_layer": "outputs/flood_extent.geojson",
    "velocity_layer": "outputs/velocity.tif",
    "risk_layer": "outputs/risk.geojson"
}
```

Use `None` when a value has not actually been calculated. Never substitute fake values.

## Status Values

```text
created
validated
preparing
running
post_processing
completed
failed
```
