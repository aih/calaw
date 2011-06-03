# Overview of sed transformations
# 1.  First convert section from text to html using txt2html Perl module and these options:
# txt2html --explicit_headings --indent_par_break --make_tables --make_anchors --xhtml  --outfile /path/to/file.html /path/to/file

# 2. Next use this script from the command-line with the following syntax:
#    ssed -R -n -f secparse.sed <filein.html >fileout.html

# 3. Convert TOC pages to html
#    Then clean up, by removing the <pre> elements, and adding appropriate breaks
#    ssed -R -i '/TABLE\sOF\sCONTENTS/,${s/<\/?pre>//; /<\/p>/! s/(.*)$/\1<br\/>/}'

# 4. Run the sed script in secparse2.sed to add links for the 29 CA Codes

# Sed transformations for creating div and spans for legislative sections.
# Using Perl Regex (-R) with the SuperSed variation on sed

#Print all lines until the first section number; 
#Add a <div> to contain the text before the first section number
1,/^<p>(?:&Yacute;)?[1-9]\d*\.([1-9]\d*\.)?/{
  s/<body>/<body>\n<div class="intro">/
  /(^<p>(?:&Yacute;)?[1-9]\d*\.(\d*\.)?)/! {
  p;
 }
}

#Act on all lines from first section number to end of file
/^<p>(?:&Yacute;)?[1-9]\d*\.(\d*\.)?/,$ {

    #Place section number in the 'hold' with a marker (xyx) on either side
    /^<p>(?:&Yacute;)?[1-9]\d*\.(\d*\.)?/ {
      h;
      s/^<p>((?:Yacute;)?[1-9]\d*\.(\d*\.)?)(.*)/xyx\1xyx/;
      x;
     
      #Add </div><div> and a <span> to the sections of the form ###.###
      s/^<p>([1-9]\d*)\.((\d*\.)+)/<\/div>\n<div class="level-1-1" id="divsec-\1\.\2">\n<p><span class="section level1-1" id="sec-\1\.\2">\1\.\2<\/span>/
      
      #Add </div><div> and a <span> to the sections of the form ###.
      s/^<p>([1-9]\d*)\./<\/div>\n<div class="level-1" id="divsec-\1\.">\n<p><span class="section level1" id="sec-\1\.">\1\.<\/span>/
      
      #Add a <span> to the (a) subsection that directly follows the section number
      s/(((\d*\.)+)<\/span>\s*)\(a\)/\1<span=class "section level-1-a" id="\2-a">\(a\)<\/span>/
      
      p;
      d;
    }
     
      #Add a newline and the section number, from the hold, to the end of the line
      G;

      #Add a <span> to lettered subdivisions on their own line, (a), (b), (c) etc.
      s/(<br\/>&nbsp;&nbsp;&nbsp;)(\(([a-z]{1,2})\))(.*)\nxyx(.*)xyx/\1<span class="subdivision level-1-a" id="\5-\3">\2<\/span>\4/

      #Add a <span> to numbered paragraphs, (1), (2), (3) etc.
      #TODO: Currently without ID and para number in class
      #       First context: \([a-z]{1,2}\)<\/span>\s*(\d{1,2})
      s/(\([a-z]{1,2}\)<\/span>\s*)(\((\d{1,2})\))/\1<span class="para para\3 level-1-a-1" >\2<\/span>/

      #Second context: <br\/>&nbsp;&nbsp;&nbsp;\(\d{1,2}\)
      #Currently without ID and para number put in class 
      s/(<br\/>&nbsp;&nbsp;&nbsp;)(\((\d{1,2})\))/\1<span class="para para\3 level-1-a-1" >\2<\/span>/
    
      #Strip the section number from any remaining lines
      s/(.*)\nxyx(.*)xyx/\1/
      
      #Hack to add </div> at the end of the last section by adding it before the </body> element
      #TODO: identify the last section and add </div> at the end
      s/<\/body>/<\/div>\n\n<\/body>/

      #Print all lines from the above categories (i.e. not sections of the form ###.*)
      p;
} 

