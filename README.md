This DDNS Update script is meant to update ddns records hosted on Namecheap.com

The script uses ipecho.net/plain to get the external ip address and reads a domains.config
file to update each domain in the file. A log file is also created and its maximum size can be set.
WHen the file grows beyond its maximum it will be trimmed from the head while new log messages
will be appended to the tail (end). 

Complete developer and User Manuals are provided in the docs directory.
