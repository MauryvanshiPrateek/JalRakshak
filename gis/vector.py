"""
Vector GIS data for the JalRakshak demo study area.

All data is SAMPLE / MOCK data — not real surveyed data.
Source: illustrative points generated from approximate Hirakud Dam
        downstream corridor in Odisha, India.
CRS: EPSG:4326 (WGS84)
License: Demo only — not for operational use.
"""
from __future__ import annotations


def get_settlements_geojson() -> dict:
    """
    Return a GeoJSON FeatureCollection of sample settlements in the
    Hirakud Dam downstream study area.

    ⚠️  DEMO DATA — positions are approximate illustrative placeholders.
    """
    features = [
        _settlement("Sambalpur Urban Area", 83.968, 21.467, population=335000, type_="City"),
        _settlement("Hirakud Township", 83.879, 21.524, population=18000, type_="Town"),
        _settlement("Burla", 83.878, 21.503, population=52000, type_="Town"),
        _settlement("Jharsuguda Road Area", 83.950, 21.535, population=12000, type_="Town"),
        _settlement("Redhakhol Area", 84.250, 21.410, population=9000, type_="Town"),
        _settlement("Sonepur", 83.918, 20.830, population=31000, type_="Town"),
        _settlement("Barpali", 83.588, 21.195, population=21000, type_="Town"),
        _settlement("Padampur", 83.063, 20.996, population=11000, type_="Town"),
        _settlement("Village-1", 83.920, 21.490, population=3500, type_="Village"),
        _settlement("Village-2", 84.010, 21.460, population=2800, type_="Village"),
        _settlement("Village-3", 84.090, 21.440, population=1900, type_="Village"),
        _settlement("Village-4", 84.170, 21.420, population=4200, type_="Village"),
        _settlement("Village-5", 84.230, 21.400, population=3100, type_="Village"),
        _settlement("Village-6", 84.310, 21.385, population=2600, type_="Village"),
        _settlement("Village-7", 84.390, 21.370, population=1500, type_="Village"),
        _settlement("Village-8", 84.480, 21.358, population=2000, type_="Village"),
    ]
    return {"type": "FeatureCollection", "features": features}


def get_roads_geojson() -> dict:
    """
    Return a GeoJSON FeatureCollection of sample road lines in the study area.

    ⚠️  DEMO DATA — route alignments are approximate illustrative placeholders.
    """
    features = [
        _road(
            "NH-53 (Sambalpur–Raipur)",
            [
                [83.870, 21.530],
                [83.940, 21.510],
                [84.010, 21.475],
                [84.120, 21.450],
                [84.300, 21.420],
                [84.490, 21.400],
            ],
            road_type="National Highway",
        ),
        _road(
            "SH-10 (Sambalpur–Jharsuguda)",
            [
                [83.875, 21.525],
                [83.900, 21.545],
                [83.960, 21.560],
                [84.020, 21.570],
            ],
            road_type="State Highway",
        ),
        _road(
            "Local Road - Burla to Sambalpur",
            [
                [83.878, 21.503],
                [83.900, 21.490],
                [83.930, 21.475],
                [83.965, 21.468],
            ],
            road_type="District Road",
        ),
        _road(
            "Riverside Road",
            [
                [83.880, 21.520],
                [83.920, 21.505],
                [83.970, 21.485],
                [84.040, 21.462],
            ],
            road_type="Rural Road",
        ),
    ]
    return {"type": "FeatureCollection", "features": features}


def get_dam_geojson(lat: float, lon: float, name: str) -> dict:
    """Return a GeoJSON point for the dam location."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {"name": name, "type": "dam"},
            }
        ],
    }


def get_river_geojson(centreline_coords: list[list[float]]) -> dict:
    """Return a GeoJSON LineString for the river centreline."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": centreline_coords},
                "properties": {"name": "Mahanadi River", "type": "river"},
            }
        ],
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _settlement(name: str, lon: float, lat: float, population: int, type_: str) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "name": name,
            "type": type_,
            "population_approx": population,
            "affected": False,
            "risk_level": "Low",
        },
    }


def _road(name: str, coords: list[list[float]], road_type: str) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "name": name,
            "road_type": road_type,
            "affected": False,
        },
    }
