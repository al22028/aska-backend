import csv
import numpy as np

def key_with_min_value(data_dict:dict) -> str:
    min_value_key = min(data_dict, key=data_dict.get)
    return min_value_key


def in_check(l:list[tuple],id:str,rc:int) -> bool:
    for tup in l:
        if tup[rc] == id:
            return True
    return False

def extract_value(l:list[tuple],row_id:str,col_id:str) -> tuple:
    for d in l:
        if d[0] == row_id :return d
        if d[1] == col_id :return d
    return ("","")

def find_page_matching() -> None:
    data = []
    with open("sandbox/zaki/data/similarity_score.csv","r",newline='') as sim:
        spamreader = csv.reader(sim,delimiter=" ",quotechar=" ")
        for r in spamreader:
            d = list(map(str,r[0].split(",")))
            data.append(d)

    t_data = np.array(data).T
    t_data = t_data.tolist()

    row_mins = [(d[0],data[0][d.index(str(min(list(map(float,d[1:])))))]) for d in data[1:]]
    col_mins = [(t_data[0][d.index(str(min(list(map(float,d[1:])))))],d[0]) for d in t_data[1:]]

    result = []

    for rows in row_mins.copy():
        if rows in col_mins:
            result.append(rows)
            row_mins.pop(row_mins.index(rows))
            col_mins.pop(col_mins.index(rows))


    for i in row_mins:
        if not in_check(result,i[0],0):
            row_pair = extract_value(row_mins,i[0],"")
            col_pair = extract_value(col_mins,i[0],"")
            if not in_check(result,row_pair[1],0) and row_pair != ("","") : result.append(row_pair)
            if not in_check(result,col_pair[1],1) and col_pair != ("","") : result.append(col_pair)

    print(result)

if __name__ == '__main__':
    find_page_matching()



