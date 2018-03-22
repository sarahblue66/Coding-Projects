＃ Challenge 2: crime-data #
# Tianyi Lan #

Firstly, make sure the csv files you want to ingest and generate report for are stored in the working directory along with all the scripts for this project.Then take a look at schema.sql to modify the directory for neighborhood data; then change the connection information(host, database, user and password to your own sql database).

Create the tables needed using the commands in schema.sql at your sql shell;
 
To ingest all data for a report for week 4, at command line, write the following commands in order:
python filter_data.py crime-base.csv | python ingest_data.py
python filter_data.py crime-week-1-patch.csv | python patch_data.py
python filter_data.py crime-week-1.csv | python ingest_data.py
python filter_data.py crime-week-2-patch.csv | python patch_data.py
python filter_data.py crime-week-2.csv | python ingest_data.py
python filter_data.py crime-week-3-patch.csv | python patch_data.py
python filter_data.py crime-week-3.csv | python ingest_data.py
python filter_data.py crime-week-4-patch.csv | python patch_data.py
python filter_data.py crime-week-4.csv | python ingest_data.py

Now you have all the data ingested into blotter table, at command line, write:
python report.py

Then you will get a popped-up graph of crime counts by day for the past month (which you can save to local locations) and a text file called ‘weekly-report.txt’ in your working directory which contains the tables generated for the report.

Aside: all rows updated by patch files will be stored in ‘updated_ids.txt’ in your working directory; all rows for which the neighborhood name was altered will be stored in ‘fixed_neighborhoods.txt’;all rows with multiple neighborhood name matches are in ‘multiple_matches.txt’; all rows with unmatched neighborhood names will be stored in ‘no_neighborhood_match.txt’; all rows that failed to ingest due to duplicated ids are stored in ‘duplicated_rows.txt’; and lastly, the ill-formatted rows with other errors that happened during ingesting and patching are stored in ‘ingest_unexpected_errors.txt’ and ‘patch_unexpected_errors.txt’, respectively.