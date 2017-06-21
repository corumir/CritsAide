# CritsAide
Python scripts to interact with the CRITs API and database.

# Requirements
* pymongo

CRITs, of course.

# Usage

```python critsaide.py 

usage: [-h] [-a TLO_type] [-g TLO_type NAME] [-d TLO_type NAME] [-r TLO_type NAME] [-c TLO_type NAME] [-q]

This program interfaces with CRITS allowing the user to get, add, and delete
TLOs as well as establish relationships between existing TLOs and adding TLOs
to current Campaigns. Be sure to set the correct hosting IP under "IP" in the
config.json file.

optional arguments:
  -h, --help            show this help message and exit
  -a  [ ...], --add  [ ...]
                        add crits TLO
  -g  [ ...], --get  [ ...]
                        get TLO from crits
  -d  [ ...], --delete  [ ...]
                        delete crits TLO
  -r  [ ...], --relationship  [ ...]
                        establish relationship between two existing TLOs
  -c  [ ...], --campaign  [ ...]
                        add TLO item to campaign
  -q, --quit            Quit program
```

If you are not running the scripts on the same system, some housekeeping is necessary. To start with, you'll need to provide remote access to the mongodb. This link, http://www.mkyong.com/mongodb/mongodb-allow-remote-access/, discusses steps to enable remote access. I'll skip repeating that here. Once you have it done, then you can test access by attempting a remote connection, for example, running:

mongo mongodb://<your ip address>:<your port, i.e. 27017>/crits
in the terminal window.
