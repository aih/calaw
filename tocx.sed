#!/bin/bash

for file in `ls | grep 'table'`;
do
     txt2html --explicit_headings --indent_par_break --make_tables --make_anchors --outfile $file"_toc.html" --xhtml $file;
     ssed -R -i -e '/<\/strong>$/ {s_([2-9][0-9.]*)(-[1-9][0-9.]*)?(</strong>)$_<a href = "/laws/target/CODE-this-\1/">\1</a>\2</strong>_}' $file"_toc.html";
     ssed -R -i -e 's_([1-9][0-9.]*)(-[1-9][0-9.]*)?$_<a href = "/laws/target/CODE-this-\1/">\1</a>\2_' $file"_toc.html";

done
