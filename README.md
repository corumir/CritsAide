# CritsAide
Python scripts to interact with the CRITs API and database. As an introduction, this is a series of python scripts that interact CRITS and the database.  Now CRITs stands for Collaborative Research Into Threats and it exposes an authenticated API, which is Automated Program Interface to allow users to talk to it from the command line.  So, these scripts are a way for you to interact with your CRITs instance without actually going into it.  You can talk to it from a command line and you'll find that it'll allow you to add every top level object in CRITs and also to make up dates and create relationships and so on.  In some instances, it doesn't use the API, but instead interacts directly with the database, for efficiency purposes (i.e. either the API didn't provide the authenticated ability or it was too slow).  

# Requirements
* pymongo
* requests

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

Help is pretty straight forward.  -a is how you add.  The syntax is -a, space, the top-level object (TLO), enter (i.e. the main IP indicator). It will prompt you for more information at that point.  It will then prompt you for more information.  

The idea behind this is to use the command-line interface to talk to CRITs and practically enter information.  It is NOT meant for a mass upload of information.  It is meant for an infinite response style of interaction, or where you are providing context and links to correlate individual pieces of data from the command line.  So, as a workflow, scripts are meant to add an item and then create relationships with other items that either you are going to add or that already exist.  For example, you might add a domain that you are interested in and then create a relationship from that domain to an IP address, and add WHOIS data to your domain, add ownership data to your domain, and so on.  

If you are not running the scripts on the same system, some housekeeping is necessary. To start with, you'll need to provide remote access to the mongodb. This link, http://www.mkyong.com/mongodb/mongodb-allow-remote-access/, discusses steps to enable remote access. I'll skip repeating that here. Once you have it done, then you can test access by attempting a remote connection, for example, running:

mongo mongodb://<your ip address>:<your port, i.e. 27017>/crits
in the terminal window.
