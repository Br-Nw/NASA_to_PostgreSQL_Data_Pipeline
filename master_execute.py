# This script is the master orchestration script that executes all the ingestion, transformation and loading scripts into 
# PostgreSQL in order.
 
import os
from dotenv import load_dotenv
from create_pg_tables import create_spec_tables

# .env file setup
load_dotenv()
exodb_url = os.getenv("DATABASE_URL")

# Step 1: create spectra tables
result = create_spec_tables(exodb_url)
print(result)