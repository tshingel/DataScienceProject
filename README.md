DataScienceProject
==================
## Recommender System

To run main_project.py, download and save the following files to the same directory: 

https://s3.amazonaws.com/LikesData/likes.csv

https://s3.amazonaws.com/LikesData/wordsEn.txt

1. main_project.py is the Python module containing all functions necessary to implement histogram plots and recommendations. main_project.py is built in the form of a simple API. This is a summary of the commands it accepts through standard input:
 - Histogram
 - Pairs Histogram
 - recommend-likes likes="LikeString1,LikeString2,etc..."
 - recommend-users likes="LikeString1,LikeString2,etc..."

2. likes.csv is a file of anonymized Facebook *Like* and *Interest* data. Each row in the data file is of the format: UID, Like1, Like2, etc. The size of the file is approximately 1GB. The data is noisy with lots of likes in foreign languages.
