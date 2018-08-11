import regex
import datetime

from database.abstraction import DCon
from mysql.connector import ProgrammingError

pairs = [
    ["Centerpartiet", "C", "Centern"], ["Kristdemokraterna", "KD"], ["Liberalerna", "L"], ["Miljöpartiet", "MP"],
    ["Socialdemokraterna", "S", "Sossarna"], ["Vänsterpartiet", "V", "Vänstern"], ["Feministisktinitiativ", "FI"],
    ["Moderaterna", "M"], ["Piratpartiet", "PP"], ["Folkpartiet", "FP"], ["AFS"], ["Sverigedemokraterna", "SD"],
]


def log_relevant(long_names, short_names, slang_names, sub=None, com=None):
    found = False
    if com:
        for name_list in long_names:
            long_match = long_search(com.body, name_list)
            if long_match:
                log_comment(com, sub, long_match)
                found = True
        if not found:
            for name in short_names:
                short_match = short_search(com.body, name)
                if short_match:
                    log_comment(com, sub, short_match)
                    found = True
        if not found:
            for name in slang_names:
                slang_match = slang_search(com.body, name)
                if slang_match:
                    log_comment(com, sub, slang_match)
                    found = True
    elif sub:
        for name_list in long_names:
            long_match = long_search(sub.title + sub.selftext, name_list)
            if long_match:
                log_submission(sub, long_match)
                found = True
        if not found:
            for name in short_names:
                short_match = short_search(sub.title + sub.selftext, name)
                if short_match:
                    log_submission(sub, short_match)
                    found = True
        if not found:
            for name in slang_names:
                slang_match = slang_search(sub.title + sub.selftext, name)
                if slang_match:
                    log_submission(sub, slang_match)
                    found = True
    return found


def long_search(data, name_list):
    if len(name_list) == 2:
        match = regex.search('\\b(%s)\\s?(%s)\\b{s<3,d<3,i<20,e<6}' % (name_list[0], name_list[1]), data,
                             flags=regex.IGNORECASE)
        if match:
            return name_list[0] + name_list[1]
    else:
        match = regex.search('\\b(%s)\\b{s<3,d<3,i<20,e<6}' % (name_list[0],), data,
                             flags=regex.IGNORECASE)
        if match:
            return name_list[0]
    return False


def short_search(data, name):
    if len(name) == 1:
        match = regex.search('\\b(%s)\\W{s<1,d<1,i<1,e<1}' % (name,), data,
                             flags=regex.FULLCASE)
        if match:
            return name
    else:
        match = regex.search('\\b(%s){s<1,d<1,i<1,e<1}' % (name,), data,
                             flags=regex.FULLCASE)
        if match:
            return name
    return False


def slang_search(data, nickname):
    match = regex.search('\\b(%s)\\b{e<1}' % (nickname,), data,
                         flags=regex.IGNORECASE)
    if match:
        return nickname
    return False


def trawl_input():
    pass


def log_submission(sub, party):
    con = DCon("swepol")
    sub.title = sub.title.replace("'", r"\'")
    sub.selftext = sub.selftext.replace("'", r"\'")

    found_sub = con.select_where("swepol_subs", ["sub_id"], [sub.id])[0]
    if not found_sub["sub_id"]:
        tries = 0
        while tries < 3:
            tries += 1
            try:
                con.insert_values("swepol_subs",
                                  "sub_title, sub_url, sub_party, sub_id, sub_author, sub_body, sub_score, " +
                                  "sub_subreddit, sub_created",
                                  [
                                      sub.title, sub.url, party, sub.id, sub.author, sub.selftext, sub.score,
                                      sub.subreddit, datetime.datetime.fromtimestamp(sub.created_utc),
                                  ])
                del con
                return True
            except ProgrammingError as err:
                print(err)
                print("Error in submission insertion, retrying...")
                del con
                con = DCon("swepol")
                continue

    del con
    return False


def log_comment(com, sub, party):
    con = DCon("swepol")

    found_sub = con.select_where("swepol_subs", ["sub_id"], [sub.id])[0]
    if not found_sub["sub_id"]:
        log_submission(sub, None)
        del con
        con = DCon("swepol")
        found_sub = con.select_where("swepol_subs", ["sub_id"], [sub.id])[0]

    found_com = con.select_where("swepol_coms", ["com_id"], [com.id])
    found_ids = list()
    found_parties = list()
    for query_com in found_com:
        if query_com["com_id"] and query_com["com_id"] not in found_ids:
            found_ids.append(query_com["com_id"])
        if query_com["com_id"] and query_com["com_party"] not in found_parties:
            found_parties += get_pairs(query_com["com_party"], pairs)
    com.body = com.body.replace("'", "")
    if com.id not in found_ids:
        created = datetime.datetime.fromtimestamp(com.created_utc)
        tries = 0
        while tries < 3:
            tries += 1
            try:
                con.insert_values("swepol_coms",
                                  "com_id, com_url, com_author, com_body, com_score, com_subreddit, com_created, " +
                                  "com_party, POSTREFID",
                                  [
                                      com.id, sub.url, com.author, com.body, com.score, com.subreddit, created,
                                      party, found_sub["sub_id"],
                                  ])
                del con
                return True
            except ProgrammingError as err:
                print(err)
                print("Error in comment insertion, retrying...")
                print(com.body)
                del con
                con = DCon("swepol")
                continue
    elif party not in found_parties:
        created = datetime.datetime.fromtimestamp(com.created_utc)
        tries = 0
        while tries < 3:
            tries += 1
            try:
                con.insert_values("swepol_coms",
                                  "com_id, com_url, com_author, com_body, com_score, com_subreddit, com_created, " +
                                  "com_party, POSTREFID",
                                  [
                                      com.id, sub.url, com.author, com.body, com.score, com.subreddit, created,
                                      party, found_sub["sub_id"],
                                  ])
                del con
                return True
            except ProgrammingError as err:
                print(err)
                print("Error in comment insertion, retrying...")
                com.body = com.body.replace("'", "")
                del con
                con = DCon("swepol")
                continue
    return False


def get_pairs(party, _pairs):
    for pair in _pairs:
        if party in pair:
            return pair
