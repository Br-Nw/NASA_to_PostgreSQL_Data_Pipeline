# THIS IS A NASA API/TAP TO POSTGRESQL PIPELINE TO THE ARCHIVE DATABASE 

import os
from dotenv import load_dotenv
from orchestrate_func import run_pipeline


# .env file setup
load_dotenv()
exodb_url = os.getenv("ARCHIVE_DATABASE_URL")

run_pipeline(exodb_url)

# This file runs the pipeline from NASA's API/TAP to the PostgreSQL archive database.
# Ideally, this should be run LESS frequently than the live database pipeline,
# which is intended for more recent data.