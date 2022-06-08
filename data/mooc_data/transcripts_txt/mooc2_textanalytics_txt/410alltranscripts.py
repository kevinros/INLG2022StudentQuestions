import glob, os



alltranscripts = open('textanalysis_alltranscripts.txt', 'w')
for file in os.listdir("/Users/assma/Documents/CS 410 Spring 2016/textanal_transcripts"):
    if file.endswith(".txt"):
    	current = open(file, 'r')
    	alltranscripts.write(current.read())

alltranscripts.close()
