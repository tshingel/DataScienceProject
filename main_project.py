import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from operator import itemgetter
import operator
from heapdict import heapdict
#import time

## number of highest frequency itms to display
TOP_HIST = 10
## y-axis step-size 
FREQ_STEP = 1000
## frequency threshold 
CUT_OFF = 6000 
## number of steps; for testing 
#STOP = 90000

def is_english_word(word, english_words):
    return word.lower() in english_words    
    
## function swaps users and likes and vice versa, e.g., for each like return a list of users         
def TransposeDic(dic):
    result = {}
    for ind, itms_list in dic.iteritems():
        for itm in itms_list:
            result.setdefault(itm, [])
            ## flip ind and itm
            result[itm].append(ind)
    return result

## likes_hist returns heap dictionary of like frequencies
## histogram dictionary: key("like" string) -> value(frequency of "like")
def likes_hist(like_users, all_likes_list):
    hd =heapdict()
    for like_id in like_users:
        key = all_likes_list[like_id]
        freq = len(like_users[like_id])  
        if freq > CUT_OFF: 
            hd[key] = -freq     
    return hd    
                         
## pairs_hist returns hash table of frequencies of like-pairs
## computed using like-frequency matrix idea    
def pairs_hist(like_users, all_likes_list, all_likes):
    ## compute frequency for each item which is greater that threshold CUT_OFF
    likes_freq = likes_hist(like_users, all_likes_list)
    ## use only likes of high frequency to compute frequency pairs 
    hd = heapdict()
    to_check = likes_freq.keys()   
    while to_check:
        itm = to_check.pop()
        s = set(like_users[all_likes[itm]])
        for other_itm in to_check:
            pair = (itm, other_itm)
            freq = len(s & (set(like_users[all_likes[other_itm]])))
            if freq > CUT_OFF: 
                hd[pair] = -freq
    return hd

## hist_plot returns histogram plot 
## cut_off is minimum frequency value 
def hist_plot(histdic): 
    #heap = [(value, key) for key, value in histdic.items()]
    # return TOP_HIST number of largest values  
    #largest = heapq.nlargest(TOP_HIST, heap)
    # reorder pairs and store them in a hash table
    n = len(histdic)
    d = {}
    if n > TOP_HIST: 
        count = TOP_HIST
    else:
        count = n    
    while count:
        pair = histdic.popitem()
        d[pair[0]] = -int(pair[1])
        count -= 1
    # reorder dictionary by values for pretty plot   
    d = OrderedDict(sorted(d.items(), key = itemgetter(1),  reverse=True))
    # plot histogram 
    fig = plt.figure()
    width = .2 
    ind = np.arange(len(d.keys()))
    plt.bar(ind, d.values(), width)
    plt.xticks(ind + width/2, d.keys())
    # take the first value in ordered dictionary 
    maxval = d.itervalues().next()
    ymax = maxval + 2 
    plt.yticks(np.arange(0, ymax, FREQ_STEP))
    # rotate x labels
    fig.autofmt_xdate()
    plt.show()   

## define similarity of two items using Jaccard index                
def similarity(dic, itm1, itm2):
    itm1_set = set(dic[itm1])
    itm2_set = set(dic[itm2])
    num_common = len(itm1_set.intersection(itm2_set))
    num_total = len(itm1_set.union(itm2_set))

    return float(num_common) / num_total

## returns list of similar items for this_itm 
def similarity_for(dic, transpose_dic, this_itm):
    # take like and collect other likes from users who liked this like
    # to_check is a set of likes to compute similarity on
    to_check = {itm 
                for ind in dic[this_itm] 
                    for itm in transpose_dic[ind]} 
    to_check.discard(this_itm)
    rankings = {itm: similarity(dic, this_itm, itm)
                for itm in to_check}
    return rankings

# return recommended list of items for given itm_list 
def recommend_likes(like_users, user_likes, itm_list): 
    total = {}
    # collect similarity scores for each item in itm_list
    for itm in itm_list:
        rankings = similarity_for(like_users, user_likes, itm)
        for other_itm in rankings:
            if not total.has_key(other_itm):
                total.setdefault(other_itm, [])
                total[other_itm].append(rankings[other_itm])
            else:
                total[other_itm].append(rankings[other_itm])
    # aggregate similarity scores for items            
    similar_itms = {key: np.mean(total[key])  
                     for key in total}
    # discard items from the itm_list
    similar_itms = {itm: ranking 
             for itm, ranking in similar_itms.items() if itm not in itm_list}
    # return sorted list of pairs (like, similarity score) starting from the largest similarity score     
    return sorted(similar_itms.iteritems(), key = operator.itemgetter(1), reverse = True)

# return similar users based on given list of likes, itm_list 
def recommend_users(like_users, user_likes, like_list):       
    # set of users who like at least one item in itm_list 
    to_check = {user for like in like_list
                    for user in like_users[like]}
    dic = {}
    sim_likes = recommend_likes(like_users, user_likes, like_list)
    ## take the largest similarity score 
    maxscore = sim_likes[0][1]
    sim_likes.reverse()
    score = maxscore 
    flag = 1
    ## collect similar likes into a list
    ## pick only those with high enough similarity score
    likes = []
    while flag:
        if sim_likes != []:
            pair = sim_likes.pop()
            score = pair[1]
            if score <= 0.5 * maxscore:
                flag = 0    
            else: 
                likes.append(pair[0])        
        else:
            flag = 0
    ## concatenate two lists              
    more_likes = like_list + likes
    ## collect all users who like likes from more_likes    
    user_list = {user for like in more_likes
                    for user in like_users[like]}
    for this_user in user_list:
        users_comp = {user for like in user_likes[this_user]
                            for user in like_users[like]}
        # compute similarity between likes_list and user_likes[this_user]
        num_common = len(to_check.intersection(users_comp)) 
        num_total = len(to_check.union(users_comp))
        dic[this_user] = float(num_common) / num_total     
    return sorted(dic.iteritems(), key = operator.itemgetter(1), reverse = True)

def main():
    with open("wordsEn.txt") as f:
        english_words = set(word.strip().lower() for word in f) ## set of all English words 

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
        for line in csv.reader(f, delimiter =',', quotechar = '"'): # line is a list of strings  
            lst = []
            for like in line[1:]:
                like_words = like.strip().split()
                count = 0
                for word in like_words:
                    if is_english_word(word.lower(), english_words):
                        count += 1
                        ## if there are only English words in like, add it to the list of likes        
                if count == len(like_words):                                                        
                    if like not in all_likes:
                        like_id = len(all_likes_list)
                        ## insert unique identifier into list of likes of a user
                        lst.append(like_id)     
                        all_likes_list.append(like)
                        all_likes[like] = like_id
                    else:
                        lst.append(all_likes[like])                                                     
            if len(lst) > 0:
                IDcount = len(all_IDs_list)        
                user_likes[IDcount] = lst 
                all_IDs_list.append(line[0])                                 
            i += 1
            ## a test to stop printing
#            if i > STOP:                                      
#                break   
#     start_time = time.time()
    # hash table: key("like") -> value(list of users's IDs)  
    like_users = TransposeDic(user_likes)
#     print time.time() - start_time, "seconds"    
    cont = 1
    while cont:
        mydata = raw_input('> ')
        if mydata == 'quit':
            cont = 0
        elif mydata == 'Pairs Histogram':
            hist = pairs_hist(like_users, all_likes_list, all_likes)
            hist_plot(hist)
        elif mydata == 'Histogram':
            hist = likes_hist(like_users, all_likes_list)
            hist_plot(hist) 
        elif mydata.find("=") != -1:
            step1 = mydata.split('=')            
            strings = step1[0].split()  
            fun_name = strings[0]
            list_name =strings[1]
            step2 = step1[1].strip(" \" ").split(',')
            if list_name == "likes":
                ## parse likes, populate like_list with likes ids  
                like_list = []
                while not step2 == []:
                    like_string = step2.pop()
                    if like_string in all_likes:
                        like_list.append(all_likes[like_string])
                            
            ## recommend likes based on given set of likes 
            if fun_name == "recommend-likes":    
                if like_list != []:        
                    sim_likes = recommend_likes(like_users, user_likes, like_list)
                    print "Similar Likes:"
                    for item, score in sim_likes[:5]:
                        print "{0:10} ------> similarity score: {1:.2f}".format(all_likes_list[item], score)
                else:
                    print "Bad input: cannot determine similar likes"
                                    
            ## recommend users based on given set of likes         
            if fun_name == "recommend-users":
                if like_list != []:
                    sim_users = recommend_users(like_users, user_likes, like_list) 
                    print "Similar Users:"
                    for item, score in sim_users[:5]:
                        print "User ID: {0} with similarity score {1:.2f}".format(item, score)
                        print "All likes of this user:"
                        for like_id in user_likes[item]:
                            print "   {}".format(all_likes_list[like_id])  
                else:
                    print "Bad input: cannot determine similar users"
        else:
            print "Wrong Input."                

if __name__ == '__main__':
    main()    
    