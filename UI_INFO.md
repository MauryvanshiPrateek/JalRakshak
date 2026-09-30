# JalRakshak — UI / UX Specification

## Design Goal

The UI should feel like a professional disaster-management command dashboard rather than a college CRUD application.

Primary visual priority:

**Map > Simulation Controls > Results > Risk/Warnings**

## Main Layout

```text
┌────────────────────────────────────────────────────────────┐
│ JALRAKSHAK                         Simulation Status        │
├───────────────┬────────────────────────────────────────────┤
│ SCENARIO      │                                            │
│               │                                            │
│ Dam           │                                            │
│ [Select ▼]    │               INTERACTIVE MAP              │
│               │                                            │
│ Breach Width  │                                            │
│ [ 30 m ]      │                                            │
│               │                                            │
│ Breach Depth  │                                            │
│ [ 15 m ]      │                                            │
│               │                                            │
│ Water Level   │                                            │
│ [120 m]       │                                            │
│               │                                            │
│ Duration      │                                            │
│ [60 min]      │                                            │
│               │                                            │
│ [RUN SIMULATION]                                           │
├───────────────┴────────────────────────────────────────────┤
│ Flooded Area │ Max Depth │ Max Velocity │ Areas at Risk   │
├────────────────────────────────────────────────────────────┤
│ Timeline / Simulation Playback                             │
└────────────────────────────────────────────────────────────┘
```

## Screens

### 1. Home / Dashboard
Show:
- project name
- short description
- selected study area
- recent simulations
- start simulation button

### 2. Scenario Setup
Inputs:
- dam
- study area
- reservoir level
- breach width
- breach depth
- breach formation time
- simulation duration

Preset buttons:
- Small breach
- Medium breach
- Severe breach

### 3. Simulation Screen
Show:
- progress
- elapsed time
- current simulation status
- log summary
- cancel button if supported

### 4. Results Screen
Map layers:
- terrain
- river
- dam
- flood extent
- water depth
- velocity
- risk zones
- settlements
- roads

### 5. Risk Panel
Show:
- flooded area
- maximum depth
- maximum velocity
- affected settlements
- affected roads
- population/exposure if data is available
- warning category

### 6. Timeline
A slider:

```text
0 ──────●──────────────── 60 min
        20 min
```

Changing time should update the displayed flood layer when time-resolved outputs exist.

## Map Controls

Provide toggles:

```text
☑ Terrain
☑ River
☑ Dam
☑ Flood Extent
☑ Water Depth
☐ Velocity
☑ Risk Zones
☐ Settlements
☐ Roads
```

## Color Semantics

Use consistent disaster-map semantics:
- Flood/water: blue family
- Low risk: light/neutral
- Moderate: yellow
- High: orange
- Critical: red

Do not rely on color alone; use labels/legends for accessibility.

## UX Rules

1. Never show fake "real-time" data as if it were live.
2. Show units for every numeric parameter.
3. Validate physically impossible inputs.
4. Display simulation assumptions.
5. Show a clear legend.
6. Make errors understandable to non-technical judges.
7. Keep the map visible during result inspection.
8. Use confirmation before expensive simulations.
9. Allow downloading result layers/reports where implemented.

## Demo Flow

```text
Open Dashboard
 → Select Demo Dam
 → Choose Severe Breach
 → Adjust one parameter
 → Run Simulation
 → Show progress
 → Reveal flood extent
 → Turn on water-depth layer
 → Move timeline
 → Show affected settlements
 → Show risk KPIs
 → Show warning panel
```
