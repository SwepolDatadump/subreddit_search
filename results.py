from database.abstraction import DCon
import matplotlib.pyplot as plt

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
weights = {
    "C": 16/20, "KD": 15/15, "L": 16/20, "MP": 10/10, "S": 17/20, "V": 18/20, "FI": 5/10, "M": 19/20,
    "PP": 8/9, "FP": 1/3,
    "AFS": 19/20, "SD": 30/30,
}

con = DCon("swepol")
occurence_dict = dict()
for key in pairs:
    try:
        occurence_dict[key[1]] = float()
    except IndexError:
        occurence_dict[key[0]] = float()
for label in range(len(pairs)):
    long_com_res = int()
    short_com_res = int()
    slang_com_res = int()
    sub_res = int()
    if len(pairs[label]) > 2:
        long_com_res = len(con.select_where("swepol_coms", ["com_party"], [pairs[label][0]]))
        short_com_res = len(con.select_where("swepol_coms", ["com_party"], [pairs[label][1]]))
        slang_com_res = len(con.select_where("swepol_coms", ["com_party"], [pairs[label][2]]))
        sub_res = len(con.select_or("swepol_subs", ["sub_party", "sub_party", "sub_party"], pairs[label]))
    elif len(pairs[label]) == 2:
        long_com_res = len(con.select_where("swepol_coms", ["com_party"], [pairs[label][0]]))
        short_com_res = len(con.select_where("swepol_coms", ["com_party"], [pairs[label][1]]))
        sub_res = len(con.select_or("swepol_subs", ["sub_party", "sub_party"], pairs[label]))

    else:
        short_com_res = len(con.select_where("swepol_coms", ["com_party"], [pairs[label][0]]))
        sub_res = len(con.select_where("swepol_subs", ["sub_party"], pairs[label]))

    try:
        occurence_dict[pairs[label][1]] += (
                long_com_res + short_com_res*weights[pairs[label][1]] + slang_com_res + sub_res
        )
    except IndexError:
        occurence_dict[pairs[label][0]] += (
                long_com_res + short_com_res * weights[pairs[label][0]] + slang_com_res + sub_res
        )

print(occurence_dict["M"])

plt.bar(range(len(occurence_dict)), list(occurence_dict.values()), align='center')
plt.xticks(range(len(occurence_dict)), list(occurence_dict.keys()))
plt.show()
