Please note that we offer a very easy to use user interface at https://maq-observations.nl/ to download data (https://maq-observations.nl/data-downloads/) and plot graphs (https://maq-observations.nl/data-figures/). The scripts provided here can be used for users who are experienced with Python (requests), or who want to automate specific processes based on the MAQ-Observations.nl database.

Post-processing/analysis scripts/files for MAQ-Observations:

- Download_Data.py: To specify user input, request data from database and save to a .csv file. This needs to be tested for other cases.
      - fetch_data.py: Function to fetch data used in Download_Data.py
- Plot_Figures.py: To specify user input and plot requested input to graphs. This is still under construction.
      - generate_graphs.py: Function to generate graphs data used in Plot_Figures.py
- Tests.py: Very simple json requests to the database, also provided on https://maq-observations.nl/api/.
- Instrument_List_v1.1.xlsx: Meta-data information on the MAQ-Observations.nl database, also available at https://maq-observations.nl/instruments/.
- MAQ-Observations_request.csv: Example file resulting from the Download_Data.ipynb notebook.

Misc folder:
Random post-processing scripts using the data from MAQ-Obsevations, not part of the core post-processing package.

Please reach out to observations.maq@wur.nl in case of specific questions or requests.
