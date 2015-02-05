#!/bin/sh

sqlite3 scraper/db.sqlite3 <<EOF
.mode csv
select query_name, legal_name, sec_number from custom_scraper_iapdfirm;
EOF
 
