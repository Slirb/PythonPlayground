import psycopg2 #PostgreSQL connector
import psycopg2.extras #Allows use of dict and named cursors
import wordfunctions
import re

wordFunc = wordfunctions

#DB connection params
conn = psycopg2.connect(
    host="localhost",
    database="PyReddit",
    user="Vance",
    password="Slirb007")


#Create named cursors for the db connection
#can access the fields by curname.fieldname
cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
subcur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

#Get all the comments for parsing
cur.execute("SELECT uniqueid, commentname, body, threadid, author FROM comments")

# Loop through stretching each word and rebuilding
for comment in cur: 

    # First we see if we need to process this comment, if it is already in the db
    # then we should save processing and not stretch the words
    subcur.execute("SELECT uniqueid FROM comments_modified WHERE commentname = %s;", (comment.commentname,))
    commentid = subcur.fetchone()
    if commentid == None:

        bodystring = comment.body.replace("\n",chr(2)) # Replace the line breaks with char 2 for proper processing
        
        # Build the list of words for processing
        wordlist = bodystring.split()

        # Loop through that list replacing as needed
        for idx, x in enumerate(wordlist):

            # Skip the char 2  for line breaks
            if x == chr(2):
                next
            
            # Use a temp variable to hold the word
            wordString = x

            # Use regex to only get the word from this 
            res = re.findall(r'\w+', wordString)

            # Loop through the words in this replacing the values in the original string
            # with the streched versions. This is to work properly with words with -, ", ', (, ), etc
            for ridx, r in enumerate(res):
                wordString = wordString.replace(r, wordFunc.stretchWord(r))

            wordlist[idx] = wordString

        # Rebuild the text from the changed list and then put the line breaks back into it
        outputList = " ".join(wordlist)
        outputList = outputList.replace(chr(2), "\n")
        
        # Now we add this to the db        
        sqlQuery = "INSERT INTO comments_modified (body, commentname, threadid, author) VALUES (%s, %s, %s, %s);"
        
        #Insert the record into the db
        subcur.execute(sqlQuery,(outputList, comment.commentname, comment.threadid, comment.author))
        conn.commit() 

#Close the db conenction
cur.close()
subcur.close()
conn.close()

