# This script is the master orchestration script that executes all the ingestion, transformation and loading scripts into 
# PostgreSQL in order.

from first_api_call_df_creation import nasa_get
from second_create_pg_tables import create_spec_tables
from third_load_dim_tables import load_dim_tables
from fourth_load_fact_table import load_spectra_fact_table
import requests
import pandas as pd
from io import StringIO

def run_pipeline(exodb_url):

    #Step 1: Call NASA API/TAP for exoplanet data and create spectra_dataframe
    nasa_get()
    response = nasa_get()
    response.raise_for_status() # Error Handling 
    status_code = f"\nHTTP status_code: {response.status_code}" # Status code for validation.
    print(status_code)
    spectra_dataframe = pd.read_csv(StringIO(response.text)) # string IO Treats text string as a file and creates spectra_dataframe data frame.

    # Step 2: Create spectra tables in PostgreSQL
    result = create_spec_tables(exodb_url)
    print(result)

    # Step 3: Load in the dim table data into PostgreSQL
    loaded = load_dim_tables(spectra_dataframe, exodb_url)
    print(loaded)

    #Step 4: Load in the spectra fact table data into PostgreSQL
    spectra_loaded = load_spectra_fact_table(spectra_dataframe, exodb_url)
    print(spectra_loaded)