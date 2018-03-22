# Tianyi Lan #
# Challenge2: crime－data #

CREATE TABLE blotter(
	id integer UNIQUE PRIMARY KEY,
	report_name text,
	section text,
	description text,
	arrest_time TIMESTAMP,
	address text,
	neighborhood text REFERENCES neighborhoods(hood),
	zone integer
);

CREATE TABLE neighborhoods(
	intptlat10 numeric,
	intptlon10 numeric,
	hood text UNIQUE,
	hood_no integer,
	acres numeric,
	sqmiles numeric
);

# Modify the path if necessary
\copy neighborhoods FROM '~/Desktop/s750/problem-bank/Data/crime-data/police-neighborhoods.csv' WITH DELIMITER ',' CSV HEADER;