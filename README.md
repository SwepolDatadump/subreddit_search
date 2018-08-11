# subreddit_search

long_names = [
    ["Center", "partiet"], ["Krist", "demokraterna"], ["Liberalerna"], ["Miljö", "partiet"], ["Moderaterna"],
    ["Social", "demokraterna"], ["Sverige", "demokraterna"], ["Vänster", "partiet"], ["Feministiskt", "initiativ"],
    ["Pirat", "partiet"], ["Folk", "partiet"]
]



short_names = [
    "KD", "MP", "SD", "FI", "PP", "L", "M", "S", "C", "AFS", "FP", "V"
]



pairs = [
    ["Centerpartiet", "C", "Centern"], ["Kristdemokraterna", "KD"], ["Liberalerna", "L"], ["Miljöpartiet", "MP"],
    ["Socialdemokraterna", "S", "Sossarna"], ["Vänsterpartiet", "V", "Vänstern"], ["Feministisktinitiativ", "FI"],
    ["Moderaterna", "M"], ["Piratpartiet", "PP"], ["Folkpartiet", "FP"], ["AFS"], ["Sverigedemokraterna", "SD"],
]


#weighted from sampling databases, long names and slang names were not found to be wrong even once on sampling, only short names
have therefore been assigned weight.


weights = {
    "C": 16/20, "KD": 15/15, "L": 16/20, "MP": 10/10, "S": 17/20, "V": 18/20, "FI": 5/10, "M": 19/20,
    "PP": 8/9, "FP": 1/3,
    "AFS": 19/20, "SD": 30/30,
}
 
 
A MySQL database need to be setup to run the code, nothing else required. Run init_db.py to get the same layout as I have.
