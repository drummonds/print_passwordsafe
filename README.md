# print_passwordsafe
Python code to convert a password safe to nicely formtated Excel document.

This can then be printed out for a hard copy.  

# Why?
In my office I use password safe and I have it backed up.  

However even though they have instructions it is beyond the 
rest of the office so they will only use a paper record.

# Why export XML and not use pypwsafe?

This is a python library that reads directly psafe files
however it doesn't work on Windows at the moment and hasn't been
updated in a while.  I think it could be made to work as
pycrypto has been udpated to include Twofish.

# Why not use XSL to format XML?
I tried this but didn't get a satisfactory result for me. 
so the users were not able to clearly find passwords in the
output file.

# Converting the test file to PDF
I saved the markdown file and then (on Windows) installed Miktek and Pandoc.

Then with the following command got a reasonable PDF:
> pandoc -f markdown -t latex -o test.pdf -V geometry:"margin=1.5cm, landscape" test.markdown

A copy of this file is included.

# Why not use Markdown?
The first attempt I tried to used markdown.  To convert to PDF I tried using
pandoc.
I gave up with Panddoc and Miktek because:
  - you certianly can't merge columns eg having the notes
  in  a second line
  - \ in passwords was causing latex to crash
  - i couldn't get long text in a column which had no spaces to
  wrap.
  
I also tried pandoc an dwkhtmltopdf.  This was simpler and had really simple 
table of contents but I gave up as:
- It looked terrible (unreadable very small fonts and nothing aligned)

# Test safe
This was created with PasswordSafe on Windows see:

![](images\PasswordSafe.png)