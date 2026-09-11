# This script normalises the spectra_files table and assigns the appropriate
# foreign keys to maintain data integrity

from sqlalchemy import create_engine, text
import pandas as pd

def load_spectra_fact_table(spectra_dataframe, exodb_url):

    engine = create_engine(exodb_url)

    with engine.begin() as conn:
        # This section of code grabs the look up tables back from PostgreSQL and assigns them to dataframes.
        planets_df = pd.read_sql("SELECT * FROM planets;", conn)
        publications_df = pd.read_sql("SELECT * FROM publications;", conn)
        spec_types_df = pd.read_sql("SELECT * FROM spec_types;", conn)
        facilities_df = pd.read_sql("SELECT * FROM facilities;", conn)
        instruments_df = pd.read_sql("SELECT * FROM instruments;", conn)

        exo_df = spectra_dataframe
        exo_df["id"] = exo_df.index + 1 # The id column of this intermediary dataframe is set to start at 1 not 0 (1 more than the index).

        for i in range(len(exo_df)): # Iterates over each record in exo_df.

            record = exo_df.iloc[i] # This is a single row from the spectra_files table grabbed from NASA's API/TAP service.

            # Extract the relevant planet, publication, spectroscopy type, facility,
            # and instrument information from each record for database insertions.
            record_planet = record["pl_name"]
            record_publication = record[["authors", "bibcode"]]
            record_spec_type = record["spec_type"]
            record_facility = record["facility"]
            record_instrument = record["instrument"]

            # This section of the code matches each record to the corresponding IDs in the related tables,
            # then extract and convert the required spectral data fields for insertion
            # into the spectra_files table
            # if it is a Null or None value it is set to None.

            pl_id = planets_df.loc[planets_df["pl_name"] == record_planet]["id"].values
            if len(pl_id) == 0:
                planet_id = None
            else:
                planet_id = int(pl_id[0])

            spec_id = spec_types_df.loc[spec_types_df["spec_type"] == record_spec_type]["id"].values
            if len(spec_id) == 0:
                spec_types_id = None
            else:
                spec_types_id = int(spec_id[0])

            pub_id = publications_df.loc[(publications_df["authors"] == record_publication["authors"]) & (publications_df["bibcode"] == record_publication["bibcode"])]["id"].values
            if len(pub_id) == 0:
                publication_id = None
            else:
                publication_id = int(pub_id[0])

            instrument_id = instruments_df.loc[instruments_df["instrument"] == record_instrument]["id"].values
            if len(instrument_id) == 0:
                instrument_id = None
            else:
                instrument_id = int(instrument_id[0])

            facility_id = facilities_df.loc[facilities_df["facility"] == record_facility]["id"].values
            if len(facility_id) == 0:
                facility_id = None
            else:
                facility_id = int(facility_id[0])

            minwavelength = float(record["minwavelng"])
            maxwavelength = float(record["maxwavelng"])
            mintranmid = float(record["mintranmid"])
            maxtranmid = float(record["maxtranmid"])
            note = record["note"]
            spec_path = record["spec_path"]

            # This section of the code uses parameterised queries to assign the set variables to their corresponding columns.
            conn.execute(text(
                '''INSERT INTO spectra_files values ( 
                    :id,
                    :planets_id,
                    :spec_types_id,
                    :publications_id,
                    :num_datapoints,
                    :instruments_id,
                    :facilities_id,
                    :minwavelng,
                    :maxwavelng,
                    :mintranmid,
                    :maxtranmid,
                    :note,
                    :spec_path);'''),

                    {'id':int(record["id"]),
                    'planets_id':planet_id,
                    'spec_types_id': spec_types_id,
                    'publications_id':publication_id,
                    'num_datapoints':int(record["num_datapoints"]),
                    'instruments_id':instrument_id,
                    'facilities_id':facility_id,
                    'minwavelng':minwavelength,
                    'maxwavelng':maxwavelength,
                    'mintranmid':mintranmid,
                    'maxtranmid':maxtranmid,
                    'note':note,
                    'spec_path':spec_path
                    })

            # Counts the number of records inserted into spectra_files table and returns it for validation.
            count_df = pd.read_sql('''SELECT COUNT(*) AS number_of_records FROM spectra_files;''', conn)
            number_of_records_series = count_df.iloc[0].values
            record_count = int(number_of_records_series[0])
    return f"\n\n---Spectra_files inserted into PostgreSQL---\n\n---{record_count} records inserted into spectra_files table in PostgreSQL---\n\n-----Fact table inserted into PostgreSQL-----"