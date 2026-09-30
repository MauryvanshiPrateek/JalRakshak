"""
Study area domain definition for the JalRakshak demo scenario.

Demo location: Hirakud Dam → Mahanadi River → Sambalpur region, Odisha, India.

All coordinates are in WGS84 (EPSG:4326).
"""

# ---------------------------------------------------------------------------
# Hirakud Dam — approximate location
# ---------------------------------------------------------------------------
DAM_LAT = 21.525
DAM_LON = 83.873
DAM_NAME = "Hirakud Dam"

# ---------------------------------------------------------------------------
# Study area bounding box (approximately 80 km downstream)
# ---------------------------------------------------------------------------
STUDY_BBOX = {
    "min_lat": 21.30,
    "max_lat": 21.75,
    "min_lon": 83.70,
    "max_lon": 84.60,
}

STUDY_CENTER_LAT = (STUDY_BBOX["min_lat"] + STUDY_BBOX["max_lat"]) / 2
STUDY_CENTER_LON = (STUDY_BBOX["min_lon"] + STUDY_BBOX["max_lon"]) / 2

# Approximate downstream river centreline waypoints (WGS84)
MAHANADI_CENTRELINE = [
    [83.873, 21.525],  # Dam
    [83.900, 21.510],
    [83.950, 21.490],
    [84.010, 21.470],
    [84.080, 21.450],
    [84.150, 21.430],
    [84.220, 21.410],
    [84.300, 21.395],
    [84.380, 21.380],
    [84.450, 21.365],
    [84.530, 21.350],
    [84.600, 21.340],
]

# Flood propagation speed factor per breach severity (illustrative)
SEVERITY_SCALE = {
    "Small": 0.30,
    "Medium": 0.60,
    "Severe": 1.00,
}
