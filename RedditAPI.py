#   Returns all of the comments for the selected subreddit
#
import praw #Reddit api handling Object
import json
import psycopg2 #PostgreSQL connector

#DB connection params
conn = psycopg2.connect(
    host="localhost",
    database="PyReddit",
    user="Vance",
    password="Slirb007")

#Variables to instantiate the praw object
clientSecret = "3E9JfLWnPuW7de7DfV0WfSqeNPHs4w"
clientID = "kf36NLXh-iX10g"
password = "1Jigg@w@tt"
userName = "Slirb"
userAgent = "Python test script (by /u/Slirb)"

#Connect to the DB
cur = conn.cursor()

#Instantiate the praw object
reddit = praw.Reddit(client_id = clientID, client_secret = clientSecret,
                     password = password, user_agent = userAgent,
                     username = userName)                     

#Print Username after valid connection
print(reddit.user.me())

#Get a subreddit by name
subreddit = reddit.subreddit("")

#see if we have an existing record, if not add it to the db
cur.execute("SELECT uniqueid FROM subreddits WHERE subreddit = %s", (subreddit.display_name,))

subredditID = cur.fetchone()
if subredditID == None:
    sqlQuery = "INSERT INTO subreddits (subreddit, url) VALUES (%s, %s);"
    
    #Insert the record into the db
    cur.execute(sqlQuery,(subreddit.display_name, subreddit.url))
    conn.commit()

    #Retrieve the fresh record for later
    cur.execute("SELECT uniqueid FROM subreddits WHERE subreddit = %s;", (subreddit.display_name,))

    subredditID = cur.fetchone()
    
print(subredditID)
#print(subreddit.display_name)  
#print(subreddit.title)         
#print(subreddit.description) 

iCount = 1
list_of_items = []
fields = ('author','body')
subfielddict = {
  "author": "name"
}

#Get the hot submissions. 
for submission in subreddit.hot(limit=200) :
    
    #We only want non-stickied
    if not submission.stickied:

        #See if we need to add the thread to the db
        cur.execute("SELECT uniqueid FROM threads WHERE threadname = %s", (submission.name,))

        threadid = cur.fetchone()
        if threadid == None:
            author = vars(submission.author)
            sqlQuery = "INSERT INTO Threads (threadname, threadtitle, author, subredditid) VALUES (%s, %s, %s, %s);"
            
            #Insert the record into the db
            cur.execute(sqlQuery,(submission.name, submission.title, author["name"], subredditID))
            conn.commit()

            #Retrieve the fresh record for later
            cur.execute("SELECT uniqueid FROM threads WHERE threadname = %s;", (submission.name,))

            threadid = cur.fetchone()   

        print(threadid)    
        #print(submission.title)  # Output: the submission's title
        #print(submission.score)  # Output: the submission's score
        #print(submission.id)     # Output: the submission's ID
        #print(submission.url)    # Output: the URL the submission points to
                                # or the submission's URL if it's a self post
        
        #Sort comments and fetch the ones that are accessed via the 'Continue this thread' option
        submission.comment_sort = "best"
        submission.comments.replace_more(limit = None)
        
        #Loop through comments adding to the ist for later
        for comment in submission.comments.list():
            #Get the properties of this comment
            to_dict = vars(comment)

            sub_dict = {}

            #Use the predefined list to get only the properties we want
            for field in fields:                        # note fields has the relevant "key" names that you want from each comment
                
                #If the field is in the subfield dictionary, then we need to get the sub list to pull from for the field
                #Also only get the list if there is data- else this isn't needed
                if field in subfielddict and to_dict[field] != None:                    
                    to_dict2 = vars(to_dict[field])
                    field2 = subfielddict[field]
                    sub_dict[field] = to_dict2[field2]                       
                else:
                    sub_dict[field] = to_dict[field]         # to_dict is just a variable that is the dictionary form of each comment

            #See if we need to add the comment to the db
            cur.execute("SELECT uniqueid FROM comments WHERE commentname = %s", (comment.name,))

            commentid = cur.fetchone()
            if commentid == None:
                sqlQuery = "INSERT INTO comments (commentname, body, author, threadid) VALUES (%s, %s, %s, %s);"
                
                #Insert the record into the db
                cur.execute(sqlQuery,(comment.name, sub_dict["body"], sub_dict["author"], threadid))
                conn.commit()

                #Retrieve the fresh record for later
                cur.execute("SELECT uniqueid FROM comments WHERE commentname = %s", (comment.name,))

                commentid = cur.fetchone()   

            print(commentid)

            #Build our list for later json            
            list_of_items.append(sub_dict)
            #print(comment.author)
            #print(comment.body)   

#Close the db conenction
cur.close()
conn.close()

#Convert the list to JSON and write to a file
json_str = json.dumps(list_of_items)
with open('data.json', 'w') as f:
    json.dump(list_of_items, f)        