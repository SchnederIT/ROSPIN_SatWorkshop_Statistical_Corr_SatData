def SATCORR_im_get( oauth, type, bound_box, dimensions, time_begin, time_end, max_cc, input_bands, output_band_count, output_type, sample_manip ):
    
    input_str = "["
    for bnd in input_bands:
        input_str += f"\"{bnd}\","
    input_str += "]" 

    script = f"""
    function setup() {{
        return {{
            input: {input_str},
            output: {{ bands: {output_band_count}, sampleType: \"{output_type}\" }}
        }};
    }}

    function evaluatePixel(sample) {{ {sample_manip} }}
    """

    request = {
        "input": {
            "bounds": {
                "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                "bbox":       bound_box,
            },
            "data": [
                {
                    "type": type,
                    "dataFilter": {
                        "timeRange": {
                            "from": time_begin,
                            "to":   time_end,
                        },
                        "maxCloudCoverage": max_cc
                    }
                }
            ],
        },
        "output": {
            "width":  dimensions[ 0 ],
            "height": dimensions[ 1 ],
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/tiff"
                    }
                }
            ]
        },
        "evalscript": script,
    }

    url = "https://sh.dataspace.copernicus.eu/api/v1/process"
    response = oauth.post( url, json=request )
    
    if response.status_code == 200:
        return response.content

    print( f"SATCORR_im_get error: {response.status_code} | {response.content}" )
    return None