SELECT
    spectra_files.id,
	planets.pl_name,
	spec_types.spec_type,
	publications.authors,
	spectra_files.num_datapoints,
	instruments.instrument,
	facilities.facility,
    spectra_files.minwavelng,
    spectra_files.maxwavelng,
    spectra_files.mintranmid,
    spectra_files.maxtranmid,
    spectra_files.note,
	publications.bibcode,
    spectra_files.spec_path,
	inserted_at
FROM spectra_files

FULL OUTER JOIN planets
    ON spectra_files.planets_id = planets.id

FULL OUTER JOIN spec_types
    ON spectra_files.spec_types_id = spec_types.id

FULL OUTER JOIN publications
    ON spectra_files.publications_id = publications.id

FULL OUTER JOIN instruments
    ON spectra_files.instruments_id = instruments.id

FULL OUTER JOIN facilities
    ON spectra_files.facilities_id = facilities.id;

-- This SQL script performs joins to reconstruct the Atmospheric Spectra flat-table in PostgreSQL. 