from tools.SATCORR_im_get import SATCORR_im_get

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# PASTE HERE api_creds.txt

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token', client_secret=client_secret, include_client_id=True)

resp = oauth.get("https://sh.dataspace.copernicus.eu/configuration/v1/wms/instances")


image = SATCORR_im_get( 
    oauth             = oauth, 
    type              = "sentinel-1-grd", 
    bound_box         = [ 23.474350,46.677239,23.716736,46.830603 ], 
    dimensions        = [ 2500, 2500 ],
    time_begin        = "2025-10-01T00:00:00Z",
    time_end          = "2025-10-30T00:00:00Z",
    max_cc            = 100,
    input_bands       =  [ "VV" ],
    output_band_count = 1,
    output_type       = "AUTO",
    sample_manip      = "return [ sample.VV ];"
)

import rasterio
import numpy as np
import matplotlib.pyplot as plt

with rasterio.MemoryFile(image) as memfile:
    with memfile.open() as dataset:
        img = dataset.read()

img = img.transpose(1, 2, 0)  

plt.figure(figsize=(6,6))
plt.imshow(img,cmap='gray')
plt.axis("off")
plt.show()
