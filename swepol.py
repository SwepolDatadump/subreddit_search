import praw
import time

from helpers.log_search import log_relevant

# largest = ["personalfinance", "wallstreetbets",]
relevant_subreddits = [
    "svenskpolitik", "sweden", "stockholm",  "spop", "swedishproblems", "privatEkonomi", "Nordiccountries",
    "Gothenburg", "Malmoe", "uppsala", "linkoping", "arbetarrorelsen", "Swirclejerk", "Snus", "saab",
    "Lund", "jag_ivl", "jobb", "pinsamt", "PrivatEkonomi", "Svenska", "svenskhistoria", "Fotografi",
    "sverigedemokraterna", "piratpartiet", "SWARJE", "unket", "Svenska", "TillSverige", "SweNsfw",
    "Allsvenskan", "iksdagen", "Frihet", "swedents", "Asksweddit", "intresseklubben",
]

long_names = [
    ["Center", "partiet"], ["Krist", "demokraterna"], ["Liberalerna"], ["Miljö", "partiet"], ["Moderaterna"],
    ["Social", "demokraterna"], ["Sverige", "demokraterna"], ["Vänster", "partiet"], ["Feministiskt", "initiativ"],
    ["Pirat", "partiet"], ["Folk", "partiet"]
]
short_names = [
    "KD", "MP", "SD", "FI", "PP", "L", "M", "S", "C", "AFS", "FP", "V"
]

slang_names = [
    "Sossarna", "Centern", "Vänstern"
]
reddit = praw.Reddit("bagool_bot2")

total_sub_count = 0
total_com_count = 0
found_total = 0
total_start = time.clock()
for sub_reddit in relevant_subreddits:
    start = time.clock()
    found = 0
    subreddit = reddit.subreddit(sub_reddit)
    searched_submissions = 0
    searched_comments = 0
    for submission in subreddit.top("week", limit=999):
        searched_submissions += 1
        if log_relevant(long_names, short_names, slang_names, sub=submission):
            found += 1
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            searched_comments += 1
            if log_relevant(long_names, short_names, slang_names, sub=submission, com=comment):
                found += 1
    found_total += found
    total_com_count += searched_comments
    total_sub_count += searched_submissions
    elapsed = time.clock() - start
    try:
        time_per_sub = round(elapsed / searched_submissions, 2)
    except ZeroDivisionError:
        time_per_sub = 0
    try:
        time_per_com = round(elapsed/searched_comments, 2)
    except ZeroDivisionError:
        time_per_com = 0
    print("\nCompleted search of %s, found %s matches in subreddit, %s matches overall." % (sub_reddit, found,
                                                                                            found_total))
    print("From a search of %s submissions and %s comments" % (searched_submissions, searched_comments))
    print("Search time to completion: %s, %s seconds per submission, %s second per comment" % (elapsed,
                                                                                               time_per_sub,
                                                                                               time_per_com))
total_time = round(time.clock() - total_start, 2)
print("\n Searched %s subreddits, %s submissions, %s comments, found %s matches." % (len(relevant_subreddits),
                                                                                     total_sub_count,
                                                                                     total_com_count,
                                                                                     found_total))
t_time_per_sub = round(total_time/total_sub_count, 2)
try:
    t_time_per_com = round(total_time / total_com_count, 2)
except ZeroDivisionError:
    t_time_per_com = 0
print("With % seconds per submission, and % seconds per comment, in %s total time" % (t_time_per_sub, t_time_per_com,
                                                                                      total_time))
