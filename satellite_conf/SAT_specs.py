# --- Common Parameters (Do not change per band) ---
COMMON_PARAMS = {
    "type": "sentinel-2-l2a", 
    "bound_box": [23.474350, 46.677239, 23.716736, 46.830603], 
    "dimensions": [2500, 2500],
    "time_begin": "2025-10-01T00:00:00Z",
    "time_end": "2025-10-30T00:00:00Z",
    "max_cc": 10,
    "output_band_count": 1,
    "output_type": "AUTO",
}

# --- Specific Band Parameters ---
# B11: Short-Wave Infrared (SWIR)
B11_SPEC = {
    "input_bands": ["B11"],
    "sample_manip": "return [ sample.B11 ];"
}

# B01: Coastal Aerosol (UV Proxy)
B01_SPEC = {
    "input_bands": ["B01"],
    "sample_manip": "return [ sample.B01 ];"
}

# B04: Red Band (For Vegetation studies)
B04_SPEC = {
    "input_bands": ["B04"],
    "sample_manip": "return [ sample.B04 ];"
}

