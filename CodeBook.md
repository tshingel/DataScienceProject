## Data Analysis
### Data Cleaning 

The data is cleaned with the help of the provided file of English words. Several data structures are used in processing 
the data. All UIDs are stored as strings in a list. The position of each string UID in the list is an integer UID which is a unique identifier for this string. All Likes are also stored in another list and numbered by their positions. A hash table (Python dictionary data structure) is used to store lists of Likes unique identifiers with keys being integer UIDs. Another hash table has Like strings as keys and Like integer identifiers as values.

### Histogram

Command line input "Histogram" generates a histogram of Likes data. That is, a graph is produced that displays Likes on the x-axis and frequency count on the y-axis. At most ten most frequent Likes are displayed.

### High-Frequency Pairs

Command line input "Pairs Histogram" generates histogram of high-frequency Like pairs. The produced graph has Like pairs on the x-axis and frequency count on the y-axis.

## Recommender Systems
### Recommending Likes Based on the Given Set of Likes

Command line input:
      >recommend-likes likes="LikeString1,LikeString2,LikeString3"

The recommendation is implemented according to the following steps:

-**Computing similar list of items for a given item I_0:**
