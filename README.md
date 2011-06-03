**CALAW**
California's legal codes, now with improved navigation and search.
This repository contains the python utilities used to parse the CA codes, as well as the code for the website at calaw.tabulaw.com.

It is released under the [[GNU Public License|http://www.gnu.org/licenses/gpl.html]].  At a future date, I may release it under the (more permissive) MIT license.

A general overview of the process used in developing the parsers can be found at [[blog.tabulaw.com|blog.tabulaw.com]]

I will be adding more detailed instructions on installation and use to this README. There may also be some redundant files here, which I will be culling over time.

--A few notes for now:--

Search is powered by Sphinx (assuming you've built the index).
To make Sphinx queries for index "calaw1": (from command line) 
$ search -c /path/to/sphinx_calaw.conf -i calaw1

To run the searchd daemon:
sudo nohup searchd --config /usr/local/etc/sphinx_calaw.conf --index calaw1 &

