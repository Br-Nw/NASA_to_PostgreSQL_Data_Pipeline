# ▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️(Run pipline script to live)▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️
# THIS IS A NASA API/TAP TO POSTGRESQL PIPELINE TO THE LIVE DATABASE 
import os
import datetime
from dotenv import load_dotenv
from orchestrate_func import run_pipeline


# .env file setup
load_dotenv()
exodb_url = os.getenv("LIVE_DATABASE_URL")

run_pipeline(exodb_url)

timestamp = datetime.datetime.now()
print(f"\n\n-----LIVE DATABASE UPDATED AT {timestamp}-----")

# This file runs the pipeline from NASA's API/TAP to the PostgreSQL live database.
# Ideally, this should be run MORE frequently than the archive database pipeline,
# which is intended for older data.
# ▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️▶️