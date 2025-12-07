# Sys includes
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
# User includes
from bitmap_plot.mapplot import plot_matrix_color_scale
from stat_analysis.grad_analysis import gradient_difference
from satellite_conf.SATCORR_im_get import SATCORR_im_get
import satellite_conf.SAT_specs as specs  # Import satellite payloads configuration file
#---------------------------------------------------
try:
    credentials_file = open("./credentials.txt", "r")
    for line in credentials_file.readlines():
        line_content = line.strip().split(" = ")
        if line_content[0].replace(" ", "") == 'client_id':
            client_id = line_content[1].replace("'", "")
        else:
            client_secret = line_content[1].replace("'", "")

except Exception as e:
    print(f"\n\033[91m[ ERROR ]\033[0m credential file reading aborted.")
    print(f"\033[91m[ ERROR ]\033[0m {e}")
    exit()
#---------------------------------------------------
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token', client_secret=client_secret, include_client_id=True)

resp = oauth.get("https://sh.dataspace.copernicus.eu/configuration/v1/wms/instances")
#---------------------------------------------------
def get_spectrum_img(oauth, band_spec_dict):
    params = specs.COMMON_PARAMS.copy()
    params.update(band_spec_dict)
    params["oauth"] = oauth

    raw_image_data = SATCORR_im_get(**params)

    if raw_image_data is None:
        print(f"Failed to retrieve data for band {band_spec_dict['input_bands'][0]}.")
        return np.array([]) 

    with rasterio.MemoryFile(raw_image_data) as memfile:
        with memfile.open() as dataset:
            img_data_raw = dataset.read() 

    matrix_2d = img_data_raw[0, :, :]
    
    return matrix_2d
#---------------------------------------------------
if __name__ == '__main__':
    IR_matrix = get_spectrum_img(oauth, specs.B11_SPEC)
    UV_matrix = get_spectrum_img(oauth, specs.B01_SPEC)
    Red_matrix = get_spectrum_img(oauth, specs.B04_SPEC)

    # Check if data was successfully returned before processing gradients
    if IR_matrix.size > 0 and UV_matrix.size > 0:
        # Now pass the clean 2D arrays to your gradient function
        Result = gradient_difference(IR_matrix, UV_matrix)
        
        plot_matrix_color_scale(IR_matrix, "IR")
        plot_matrix_color_scale(UV_matrix, "UV")

        plot_matrix_color_scale(Result, "UV - IR correlation")

        plt.show()
        
    else:
        print("Skipping gradient calculation due to missing data.")