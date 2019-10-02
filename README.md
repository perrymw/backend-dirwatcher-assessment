# Directory watching and logging
This program is designed to scan any entered directory on their system 
for any word that the user desires in any entered txt file.
A terminal output will keep logging, letting the user know that 
the word has been found in the file.  
Every three seconds unless specified, the program will keep polling for any change.  
A log will also report when it has started and how long the program has been 
running. The log will also include if any file has been deleted.

# Sample command:

python dirwatcher.py Test.txt 'test' 4

meaning it is looking for a txt file named Test.txt for the word test and will poll every 4 seconds
# Sample output:
2019-10-02 16:15:43,539.539 -dirwatcher.py -INFO - Watching directory: ./Test
File Extension: .txt
Magic Text: test
Polling at 3 seconds.

# If found:
2019-10-02 16:07:38,278.278 -dirwatcher.py -INFO - Found file: Test.txt
2019-10-02 16:07:38,279.279 -dirwatcher.py -INFO - test was found on  