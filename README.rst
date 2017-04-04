
Public images, pages for aikif.com

Deploy Notes
---------------------

Setup
---------------------

git remote add origin https://github.com/acutesoftware/aikif.com.git


To initialise the database, uncomment the line
     initdb_command()   
     
which builds the schema.sql     
     
Once done, start the webserver via 
    python aikif_web.py
    
(or run GO.BAT from windows)



Goals
---------------------
The core data tables (events, objects, facts, etc) should not be added to manually via the website, rather it should use mappers and programs to parse info into them.

Views / searches are then used to get useful results from those core data tables

