# This script sends a GET request to NASA's Exoplanet Archive TAP service.
# and returns the HTTP response containing the query results in CSV format.
from io import StringIO
import pandas as pd
import requests

def nasa_get():

    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync" #NASA's endpoint

    params = {
        "query": """
            SELECT *
            FROM spectra
        """,
        "format": "csv"
    } 

    # HTTP GET request to NASA API/TAP
    r = requests.get(url, params=params) # Response from NASA's API endpoint
    return r