# Data Specification

## DEM

Preferred format:
- GeoTIFF

Requirements:
- valid CRS
- elevation values in metres
- known vertical/horizontal reference
- bounded study area

## River

Accepted:
- GeoJSON
- Shapefile
- GeoPackage

Required:
- geometry
- CRS

## Dam

Accepted:
- GeoJSON
- Shapefile
- GeoPackage
- CSV with coordinates for simple demo

Required:
- location
- name/id

## Settlements / Buildings / Roads

Vector data:
- GeoJSON
- Shapefile
- GeoPackage

Each layer should document:
- source
- CRS
- date
- license
- relevant attributes

## Population / Exposure

If used, document:
- population estimate
- spatial unit
- reference date
- source
- aggregation method

## CRS Rule

All layers should be transformed to a common projected CRS appropriate for the study area before distance/area calculations.

## Data Licensing

Record the source and license for every externally obtained dataset.
