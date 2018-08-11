from database.abstraction import DCon
from mysql.connector.errors import ProgrammingError

con = DCon("swepol")

try:
    query_list = [
        "sub_title text", "sub_url VARCHAR(512)", "sub_party text", "sub_id VARCHAR(60)",
        "sub_author VARCHAR(256)", "sub_body text", "sub_score VARCHAR(60)", "sub_subreddit VARCHAR(512)",
        "sub_created TIMESTAMP", "time_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP", "PRIMARY KEY(sub_id)"
    ]
    con.create_table("swepol_subs", query_list)
    print("swedish parties submissions created.")
except ProgrammingError as err:
    print(err)

try:
    query_list = [
        "com_number int NOT NULL AUTO_INCREMENT", "com_party text",
        "com_id VARCHAR(60)", "com_url VARCHAR(512)", "com_author VARCHAR(256)", "com_body text",
        "com_score VARCHAR(60)", "com_subreddit VARCHAR(512)", "com_created TIMESTAMP",
        "time_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP", "PRIMARY KEY(com_number)",
        "POSTREFID VARCHAR(60)", "FOREIGN KEY (POSTREFID) REFERENCES swepol_subs(sub_id)"
    ]
    con.create_table("swepol_coms", query_list)
    print("swedish parties comments created.")
except ProgrammingError as err:
    print(err)

del con
