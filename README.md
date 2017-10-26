# print_passwordsafe
Python code to convert a password safe to a Markdown document.

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

# Test safe
This was created with PasswordSafe on Windows see:

![](images\PasswordSafe.png)