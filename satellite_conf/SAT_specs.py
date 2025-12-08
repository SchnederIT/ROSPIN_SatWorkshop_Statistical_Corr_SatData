#
# Primary author: Vatca T.-H.
# Co-author: Crivcianschi A.
# Date: December 2025
#

# --- Common Parameters (Do not change per band) ---
COMMON_PARAMS = {
    "type": "sentinel-2-l2a", 
    # "bound_box": [23.474350, 46.677239, 23.716736, 46.830603],\
    "bound_box" : [ -81.7729-0.5, 33.13001+0.5, -81.7729+0.5, 33.13001-0.5 ], 
    "dimensions": [2500, 2500],
    "time_begin": "2025-10-01T00:00:00Z",
    "time_end": "2025-10-30T00:00:00Z",
    "max_cc": 10,
    "output_band_count": 1,
    "output_type": "AUTO",
}

# --- Specific Band Parameters ---

# B01: Coastal Aerosol (UV Proxy, Blue end of spectrum)
B01_SPEC = {
    "input_bands": ["B01"],
    "sample_manip": "return [ sample.B01 ];"
}

# B02: Blue Band (Water Penetration, Blue/Green Algae)
B02_SPEC = {
    "input_bands": ["B02"],
    "sample_manip": "return [ sample.B02 ];"
}

# B03: Green Band (Vegetation Analysis, Peak Green Reflectance)
B03_SPEC = {
    "input_bands": ["B03"],
    "sample_manip": "return [ sample.B03 ];"
}

# B04: Red Band (For Vegetation studies, Chlorophyll Absorption)
B04_SPEC = {
    "input_bands": ["B04"],
    "sample_manip": "return [ sample.B04 ];"
}

# B08: Near-Infrared (NIR) Band (Healthiest Vegetation, Biomass)
B08_SPEC = {
    "input_bands": ["B08"],
    "sample_manip": "return [ sample.B08 ];"
}

# B11: Short-Wave Infrared 1 (SWIR 1, Moisture Content, IR)
B11_SPEC = {
    "input_bands": ["B11"],
    "sample_manip": "return [ sample.B11 ];"
}

# B12: Short-Wave Infrared 2 (SWIR 2, Geological Features, IR)
B12_SPEC = {
    "input_bands": ["B12"],
    "sample_manip": "return [ sample.B12 ];"
}

# --- Index Specifications (Pre-calculated single-band matrices) ---

# NDVI (Normalized Difference Vegetation Index)
NDVI_SPEC = {
    "input_bands": ["B08", "B04"],  # Requires two input bands
    "sample_manip": "return [ (sample.B08 - sample.B04) / (sample.B08 + sample.B04) ];",
    "output_band_count": 1,
}

# NDWI (Normalized Difference Water Index)
NDWI_SPEC = {
    "input_bands": ["B03", "B08"],
    "sample_manip": "return [ (sample.B03 - sample.B08) / (sample.B03 + sample.B08) ];",
    "output_band_count": 1,
}

# --- Multi-Band Specification (For visualization/reference) ---

# RGB_REF: True Color Composite (3 bands for visualization)
RGB_REF_SPEC = {
    "input_bands": ["B04", "B03", "B02"],  # Red, Green, Blue
    "sample_manip": "return [ 2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02 ];", # Scaling by 2.5 often improves visible contrast
    "output_band_count": 3, # CRITICAL: Must be 3 bands
}