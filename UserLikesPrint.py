## Helper Module 
## Author: Tatiana Shingel Moody
import csv
STOP = 100
   
with open("wordsEn.txt") as f:
    english_words = set(word.strip().lower() for word in f) ## set of all English words 

def is_english_word(word):
    return word.lower() in english_words    

with open('likes.csv', 'rb') as f:
    ## hash table: key(userID) -> value(list of "likes" numbered by integers as unique identifiers) 
    user_likes = {}
    ## hash table: key("like" string) -> value("like" unique identifier)                                                
    all_likes = {}
    ## list of all "likes" as strings, unique identifier -- position in the list                          
    all_likes_list = []
    ## list of all IDs as strings, unique identifier -- position in the list
    all_IDs_list = []     
    IDcount = 0
    i = 1
    ###c = 0       
    for line in csv.reader(f, delimiter =',', quotechar = '"'): # line is a list of strings  
        lst = []
        for like in line[1:]:
            like_words = like.strip().split()
            count = 0
            for word in like_words:
                if is_english_word(word.lower()):
                    count += 1
            # if there are only English words in like, add it to the list of likes        
            if count == len(like_words):                                                        
                if like not in all_likes:
                    like_id = len(all_likes_list)
                    # insert unique identifier into list of likes of a user
                    lst.append(like_id)     
                    all_likes_list.append(like)
                    ### status update for large data set
                    ###c += 1                                       
                    all_likes[like] = like_id
                    ###if c%10000==0: print "%d / %d" % (c, len(all_likes))                     
                else:
                    lst.append(all_likes[like])                                                     
        if len(lst) > 0:
            IDcount = len(all_IDs_list)        
            user_likes[IDcount] = lst     # update data dictionary 
            all_IDs_list.append(line[0])                                 
        i += 1
        if i > STOP:                      # a flag to stop printing  
            break
     
for key in user_likes:
    print "user:", key, "user's likes:"
    for like in user_likes[key]:
        print "like id", like, "like string:", all_likes_list[like]    
