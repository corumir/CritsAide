# CritsAide
Python scripts to interact with the CRITs API and database.

# Requirements
* pymongo

CRITs, of course.

If you are not running the scripts on the same system, some housekeeping is necessary. To start with, you'll need to provide remote access to the mongodb. This link, http://www.mkyong.com/mongodb/mongodb-allow-remote-access/, discusses steps to enable remote access. I'll skip repeating that here. Once you have it done, then you can test access by attempting a remote connection, for example, running:

mongo mongodb://<your ip address>:<your port, i.e. 27017>/crits
in the terminal window.
