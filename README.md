# IAPD
Extract information from IAPD (http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx)

## Setup
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

## Run
The scraper.py script assumes that the file Legal Names.xlsx is in the current directory

    $ ./scraper.py

## Get results

Use the script included in this directory to extract results from the database (scraper/db.sqlite3). 
It will pull out the query name, legal namd and SEC #:

    $ ./get_results_from_db.sh
