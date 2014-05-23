DataScienceProject
==================
## Recommender System

To run main_project.py, download and save the following files to the same directory: 

https://s3.amazonaws.com/LikesData/likes.csv

https://s3.amazonaws.com/LikesData/wordsEn.txt

1. main_project.py is a Python module which contains the functions necessary to implement histogram plots and recommendations. main_project.py is built in the form of a simple API. It accepts the following list of commands through standard input:
 - Histogram
 - Pairs Histogram
 - recommend-likes likes="LikeString1,LikeString2,etc..."
 - recommend-users likes="LikeString1,LikeString2,etc..."

2. likes.csv contains anonymized Facebook **Like** and **Interest** data. Each row in the data file is of the format: **UID, Like1, Like2**, etc. The size of the file is approximately 1GB. The data is noisy with lots of likes in foreign languages.
3. UserLikesPrint.py is a Python module which outputs User-Likes data to the console row-by-row after reading and cleaning the data from likes.csv. It is included for convenience and can be used to assemble lists of Likes data to test the code.
4. wordsEn.txt contains most common English words. 
