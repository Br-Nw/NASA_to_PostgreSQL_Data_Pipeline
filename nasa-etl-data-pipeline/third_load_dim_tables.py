# This is a script that loads all the look up data from NASA's API/TAP endpoint into the relevant postgreSQL look up/dim tables.
import requests
from sqlalchemy import create_engine, text
from io import StringIO
import pandas as pd

def load_dim_tables(spectra_dataframe, exodb_url):

    # The section of the code consists of functions which when called, insert values into the PostgreSQL tables.
    def insert_into_planets(spectra_dataframe, exodb_url):
        engine = create_engine(exodb_url) # PostgreSQL connection
        with engine.begin() as conn:
            planets = list(spectra_dataframe["pl_name"].dropna().unique()) #Transforming data by dropping nulls and ensuring uniqueness
            for planet in planets:
                conn.execute(text(f'''INSERT INTO planets(pl_name) values(:planet);'''), {"planet":planet})
        return "---Planet names inserted into PostgreSQL---"

    def insert_into_instruments(spectra_dataframe, exodb_url):
        engine = create_engine(exodb_url) # PostgreSQL connection
        with engine.begin() as conn:
                instruments = list(spectra_dataframe["instrument"].dropna().unique()) #Transforming data by dropping nulls and ensuring uniqueness
                for instrument in instruments:
                    conn.execute(text(f'''INSERT INTO instruments(instrument) values(:instrument);'''), {"instrument":instrument})
        return "---Instruments inserted into PostgreSQL---"

    def insert_into_spec_types(spectra_dataframe, exodb_url):
        engine = create_engine(exodb_url) # PostgreSQL connection
        with engine.begin() as conn:
                spec_types = list(spectra_dataframe["spec_type"].dropna().unique()) #Transforming data by dropping nulls and ensuring uniqueness
                for spec_type in spec_types:
                    conn.execute(text(f'''INSERT INTO spec_types(spec_type) values(:spec_type);'''), {"spec_type":spec_type})
        return "---Spec_types inserted into PostgreSQL---"

    def insert_into_facilities(spectra_dataframe, exodb_url):
        engine = create_engine(exodb_url)
        facilities = spectra_dataframe["facility"].dropna().unique() #Transforming data by dropping nulls and ensuring uniqueness
        with engine.begin() as conn:
            for facility in facilities:
                conn.execute(text("INSERT INTO facilities(facility) VALUES (:facility)"), {"facility": facility})
        return "---Facilities inserted into PostgreSQL---"

    def insert_into_publications(spectra_dataframe, exodb_url):
        engine = create_engine(exodb_url) # PostgreSQL connection
        with engine.begin() as conn:
                publications = publications = list(spectra_dataframe[["authors", "bibcode"]].value_counts().index)
                for i, publication in enumerate(publications):
                    author = publications[i][0] 
                    bibcode = publications[i][1]
                    conn.execute(text(f'''INSERT INTO publications(authors, bibcode) values(:authors, :bibcode);'''), {"authors":author, "bibcode":bibcode})
        return "---Publications inserted into PostgreSQL---"

    pl = insert_into_planets(spectra_dataframe, exodb_url)
    ins = insert_into_instruments(spectra_dataframe, exodb_url)
    spec = insert_into_spec_types(spectra_dataframe, exodb_url)
    fal = insert_into_facilities(spectra_dataframe, exodb_url)
    pub = insert_into_publications(spectra_dataframe, exodb_url)

    return "\n\n".join([pl, ins, spec, fal, pub, "\n-----All look up tables inserted into PostgreSQL-----"])