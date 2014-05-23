# Data Analysis
## Data Cleaning 

The data is cleaned with the help of the provided file of English words. Several data structures are used in processing 
the data. All UIDs are stored as strings in a list. The position of each string UID in the list is an integer UID which is a unique identifier for this string. All Likes are also stored in another list and numbered by their positions. A hash table (Python dictionary data structure) is used to store lists of Likes unique identifiers with keys being integer UIDs. Another hash table has Like strings as keys and Like integer identifiers as values.
