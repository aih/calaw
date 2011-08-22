##CALAW##

California's legal codes, now with improved navigation and search.
This repository contains the python utilities used to parse the CA codes, as well as the code for the website at calaw.tabulaw.com.

It is released under the [GNU Public License](http://www.gnu.org/licenses/gpl.html).  At a future date, I may release it under the (more permissive) MIT license.

A general overview of the process used in developing the parsers can be found at http://blog.tabulaw.com

I will be adding more detailed instructions on installation and use to this README. There may also be some redundant files here, which I will be culling over time.

###Setup Documentation (needs improvement):###

####Installing Packages and Dependencies:####

`sudo apt-get install build-essential;
sudo apt-get install python2.6-dev python-setuptools libxml2-dev libxslt-dev;
sudo apt-get install sphinxsearch;
sudo easy_install pip;
sudo pip install django;
sudo pip install django-sphinx;`

_Change the PORT settings in django-sphinx from 3312 to 9312, the new default for SPHINX. The PORT number is found in at least two django-sphinx files._

`sudo pip install lxml;
sudo apt-get install nginx python-flup;`

####Search Set-up####

Search is powered by Sphinx, using a branch of [django-sphinx](https://github.com/xobb1t/django-sphinx/) with an option (sphinx_only) that decouples Sphinx from the database. The Sphinx index was built from a PostgreSQL version of the project database.
To make Sphinx queries for index "calaw1": (from command line) 
`$ search -c /path/to/sphinx_calaw.conf -i calaw1`

To run the searchd daemon:

`sudo nohup searchd --config /usr/local/etc/sphinx_calaw.conf --index calaw1 &`

-----

Hosting on AWS EC2:

The site is currently hosted on an Ubuntu image on AWS EC2 by Canonical (ami-97c694d2 found on the [Alestic list of instances](http://alestic.com/))

The Nginx + fastcgi server is set up according to the following [instructions](http://wiki.nginx.org/PythonFlup)
