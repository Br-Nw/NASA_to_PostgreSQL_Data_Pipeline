# This script contains a function that when executed, creates all the fact, dimension and look up tables for the spectra_file data.

from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np 

# function that creates spectra_file tables within postgreSQL database
def create_spec_tables(PostgreSQL_DATABASE_URL):

    # PostgreSQL connection
    engine = create_engine(PostgreSQL_DATABASE_URL)

    # Execute SQL commands DDL
    with engine.begin() as conn:
        conn.execute(text('''
        DROP TABLE IF EXISTS spectra_files;
        DROP TABLE IF EXISTS planets;
        DROP TABLE IF EXISTS instruments;
        DROP TABLE IF EXISTS publications;
        DROP TABLE IF EXISTS facilities;
        DROP TABLE IF EXISTS spec_types;

        
        CREATE TABLE IF NOT EXISTS planets (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        pl_name VARCHAR UNIQUE  
        ); 

        CREATE TABLE IF NOT EXISTS instruments (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        instrument VARCHAR UNIQUE 
        );

        CREATE TABLE IF NOT EXISTS publications (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        authors VARCHAR,
        bibcode VARCHAR,
        UNIQUE (authors, bibcode)
        );

        CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        facility VARCHAR UNIQUE 
        );

        CREATE TABLE IF NOT EXISTS spec_types (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        spec_type VARCHAR UNIQUE 
        );

        CREATE TABLE IF NOT EXISTS spectra_files (
        id INTEGER PRIMARY KEY,
        planets_id INTEGER,
        spec_types_id INTEGER,
        publications_id INTEGER,
        num_datapoints INTEGER,
        instruments_id INTEGER,
        facilities_id INTEGER,
        minwavelng FLOAT,
        maxwavelng FLOAT,
        mintranmid FLOAT,
        maxtranmid FLOAT,
        note VARCHAR,
        spec_path VARCHAR UNIQUE,
        inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (planets_id) REFERENCES planets(id),
        FOREIGN KEY (spec_types_id) REFERENCES spec_types(id),
        FOREIGN KEY (publications_id) REFERENCES publications(id),
        FOREIGN KEY (instruments_id) REFERENCES instruments(id),
        FOREIGN KEY (facilities_id) REFERENCES facilities(id)
        );
        '''))
        return f'''\n\n---Tables created in PostgreSQL---\n''' 
        # Validation message saying that the tables have been created.